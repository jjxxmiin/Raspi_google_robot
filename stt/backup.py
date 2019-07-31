# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample that implements a gRPC client for the Google Assistant API."""

# -*- coding: euc-kr -*-

import RPi.GPIO as GPIO
import module_new as m
from time import sleep
import threading
import kbhit
import signal
import concurrent.futures
import json
import logging
import os
import os.path
import pathlib2 as pathlib
import sys, tty, termios
import time
import uuid
from gtts import gTTS
import pyglet
import random
import socket

import click
import grpc
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import pymysql

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
from tenacity import retry, stop_after_attempt, retry_if_exception


try:
    from . import (
        assistant_helpers,
        audio_helpers,
        browser_helpers,
        device_helpers
    )
except (SystemError, ImportError):
    import assistant_helpers
    import audio_helpers
    import browser_helpers
    import device_helpers

ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
END_OF_UTTERANCE = embedded_assistant_pb2.AssistResponse.END_OF_UTTERANCE
DIALOG_FOLLOW_ON = embedded_assistant_pb2.DialogStateOut.DIALOG_FOLLOW_ON
CLOSE_MICROPHONE = embedded_assistant_pb2.DialogStateOut.CLOSE_MICROPHONE
PLAYING = embedded_assistant_pb2.ScreenOutConfig.PLAYING
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5


class Education:
    # initialize of DB Information
    def __init__(self, host, user, dbname, passwd, ser, name):
        self.host=host
        self.user=user
        self.dbname=dbname
        self.passwd=passwd
        self.ser=ser
        self.name=name

    # DB Connect
    def connection(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.passwd,
                db=self.dbname
            )
            cur = conn.cursor()
            print('=================================')
            print('=================================')
            print('DB Connection Success')
            print('=================================')
            print('=================================')
            return conn, cur

        except:
            print('DB Connection Failed')
            exit()
        
    # Insert into isfun table
    def isfun(self, conn, cur, sText):
        try:
            sql = "INSERT INTO isfun(seq, name, ans) VALUES(%s, %s, %s)"
            cur.execute(sql, (self.ser, self.name, sText))
            conn.commit()
            print('(DB_isfun)Insert Success')

        except:
            print('(DB_isfun)Insert Failed')

    # Insert into english table
    def english(self, conn, cur, point):
        try:
            sql = "INSERT INTO english(seq, name, point) VALUES(%s, %s, %s)"
            cur.execute(sql, (self.ser, self.name, point))
            conn.commit()
            print('(DB_English)Insert Success')

        except:
            print('(DB_English)Insert Failed')

    # Insert into math table
    def math(self, conn, cur, point):
        try:
            sql = "INSERT INTO math(seq, name, point) VALUES(%s, %s, %s)"
            cur.execute(sql, (self.ser, self.name, point))
            conn.commit()
            print('(DB_Math)Insert Success')

        except:
            print('(DB_Math)Insert Failed')

    # Delete data of isfun table
    def del_isfun(self, conn, cur):
        try:
            sql = "DELETE FROM isfun"
            cur.execute(sql)
            conn.commit()
            print('(DB_isfun)Delete Success')

        except:
            print('(DB_isfun)Delete Failed')

    # Delete data of english table
    def del_english(self, conn, cur):
        try:
            sql = "DELETE FROM english"
            cur.execute(sql)
            conn.commit()
            print('(DB_English)Delete Success')

        except:
            print('(DB_English)Delete Failed')

    # Delete data of math table
    def del_math(self, conn, cur):
        try:
            sql = "DELETE FROM math"
            cur.execute(sql)
            conn.commit()
            print('(DB_Math)Delete Success')

        except:
            print('(DB_Math)Delete Failed')

    # Searching table of isfun
    def search_isfun(self, conn, cur):
        try:
            sql = "SELECT *FROM isfun"
            cur.execute(sql)
            result = cur.fetchall()

            print('<Table isfun>\n')
            print('=================================')
            for row in result:
                print(row)
            print('(DB_isfun)Searching Success')

        except:
            print('(DB_isfun)Searching Failed')

    # Searching table of english
    def search_english(self, conn, cur):
        try:
            sql = "SELECT *FROM english"
            cur.execute(sql)
            result = cur.fetchall()

            print('<Table english>\n')
            print('=================================')
            for row in result:
                print(row)
            print('(DB_english)Searching Success')

        except:
            print('(DB_english)Searching Failed')
            
    # Searching table of math
    def search_math(self, conn, cur):
        try:
            sql = "SELECT *FROM math"
            cur.execute(sql)
            result = cur.fetchall()

            print('<Table math>\n')
            print('=================================')
            for row in result:
                print(row)
            print('(DB_math)Searching Success')

        except:
            print('(DB_math)Searching Failed')

    # DB cleaner
    def dbclean(self, conn, cur):
        self.del_isfun(conn, cur)
        self.del_english(conn, cur)
        self.del_math(conn, cur)
        print('=================================')

    # DB close
    def dbclose(self, conn, cur):
        conn.close()
        cur.close()


class SampleAssistant(object):
    """Sample Assistant that supports conversations and device actions.

    Args:
      device_model_id: identifier of the device model.
      device_id: identifier of the registered device instance.
      conversation_stream(ConversationStream): audio stream
        for recording query and playing back assistant answer.
      channel: authorized gRPC channel for connection to the
        Google Assistant API.
      deadline_sec: gRPC deadline in seconds for Google Assistant API call.
      device_handler: callback for device actions.
    """

    def __init__(self, language_code, device_model_id, device_id,
                 conversation_stream, display,
                 channel, deadline_sec, device_handler):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_stream = conversation_stream
        self.display = display

        # Opaque blob provided in AssistResponse that,
        # when provided in a follow-up AssistRequest,
        # gives the Assistant a context marker within the current state
        # of the multi-Assist()-RPC "conversation".
        # This value, along with MicrophoneMode, supports a more natural
        # "conversation" with the Assistant.
        self.conversation_state = None
        # Force reset of first conversation.
        self.is_new_conversation = True

        # Create Google Assistant API gRPC client.
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec
        #self.moving = False
        self.device_handler = device_handler

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False
        self.conversation_stream.close()

    def is_grpc_error_unavailable(e):
        is_grpc_error = isinstance(e, grpc.RpcError)
        if is_grpc_error and (e.code() == grpc.StatusCode.UNAVAILABLE):
            logging.error('grpc unavailable error: %s', e)
            return True
        return False

    @retry(reraise=True, stop=stop_after_attempt(3),
           retry=retry_if_exception(is_grpc_error_unavailable))
    def assist(self,commands=None,is_respon=True):
        """Send a voice request to the Assistant and playback the response.

        Returns: True if conversation should continue.
        """
        continue_conversation = False
        moving = False
        device_actions_futures = []
        # ----
        stt_list = []
        stt_tmp = ''
        # ----
        self.conversation_stream.start_recording()
        logging.info('Recording audio request.')

        def iter_log_assist_requests():
            for c in self.gen_assist_requests():
                assistant_helpers.log_assist_request_without_audio(c)
                yield c
            logging.debug('Reached end of AssistRequest iteration.')

        # This generator yields AssistResponse proto messages
        # received from the gRPC Google Assistant API.
        for resp in self.assistant.Assist(iter_log_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            
            # voice recognition end
            if resp.event_type == END_OF_UTTERANCE:
                logging.info('End of audio request detected.')
                logging.info('Stopping recording.')
                self.conversation_stream.stop_recording()
            # stt
            if resp.speech_results:
                stt_tmp = ' '.join(r.transcript for r in resp.speech_results)
                #logging.info('Transcript of user  request: %s.',
                #             ' '.join(r.transcript
                #                      for r in resp.speech_results))
                
                if commands != None:
                    for command in commands:
                        if command in stt_tmp:
                            moving = True
                            break
            # response
            if moving == False and is_respon == True: 
                if len(resp.audio_out.audio_data) > 0:
                    if not self.conversation_stream.playing:
                        self.conversation_stream.stop_recording()
                        self.conversation_stream.start_playback()
                        logging.info('Playing assistant response.')
                    self.conversation_stream.write(resp.audio_out.audio_data)
                
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                logging.debug('Updating conversation state.')
                self.conversation_state = conversation_state
            
            if resp.dialog_state_out.volume_percentage != 0:
                volume_percentage = resp.dialog_state_out.volume_percentage
                logging.info('Setting volume to %s%%', volume_percentage)
                self.conversation_stream.volume_percentage = volume_percentage
            
            if resp.dialog_state_out.microphone_mode == DIALOG_FOLLOW_ON:
                continue_conversation = True
                logging.info('Expecting follow-on query from user.')
            elif resp.dialog_state_out.microphone_mode == CLOSE_MICROPHONE:
                continue_conversation = False
            if resp.device_action.device_request_json:
                device_request = json.loads(
                    resp.device_action.device_request_json
                )
                fs = self.device_handler(device_request)
                if fs:
                    device_actions_futures.extend(fs)
            if self.display and resp.screen_out.data:
                system_browser = browser_helpers.system_browser
                system_browser.display(resp.screen_out.data)

        if len(device_actions_futures):
            logging.info('Waiting for device executions to complete.')
            concurrent.futures.wait(device_actions_futures)

        logging.info('Finished playing assistant response.')
        self.conversation_stream.stop_playback()

        return continue_conversation, stt_tmp

    def gen_assist_requests(self):
        """Yields: AssistRequest messages to send to the API."""

        config = embedded_assistant_pb2.AssistConfig(
            audio_in_config=embedded_assistant_pb2.AudioInConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
            ),
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding='LINEAR16',
                sample_rate_hertz=self.conversation_stream.sample_rate,
                volume_percentage=self.conversation_stream.volume_percentage,
            ),
            dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                language_code=self.language_code,
                conversation_state=self.conversation_state,
                is_new_conversation=self.is_new_conversation,
            ),
            device_config=embedded_assistant_pb2.DeviceConfig(
                device_id=self.device_id,
                device_model_id=self.device_model_id,
            )
        )
        if self.display:
            config.screen_out_config.screen_mode = PLAYING
        # Continue current conversation with later requests.
        self.is_new_conversation = False
        # The first AssistRequest must contain the AssistConfig
        # and no audio data.
        yield embedded_assistant_pb2.AssistRequest(config=config)
        for data in self.conversation_stream:
            # Subsequent requests need audio data, but not config.
            yield embedded_assistant_pb2.AssistRequest(audio_in=data)



@click.command()
@click.option('--api-endpoint', default=ASSISTANT_API_ENDPOINT,
              metavar='<api endpoint>', show_default=True,
              help='Address of Google Assistant API service.')
@click.option('--credentials',
              metavar='<credentials>', show_default=True,
              default=os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json'),
              help='Path to read OAuth2 credentials.')
@click.option('--project-id',
              metavar='<project id>',
              help=('Google Developer Project ID used for registration '
                    'if --device-id is not specified'))
@click.option('--device-model-id',
              metavar='<device model id>',
              help=(('Unique device model identifier, '
                     'if not specifed, it is read from --device-config')))
@click.option('--device-id',
              metavar='<device id>',
              help=(('Unique registered device instance identifier, '
                     'if not specified, it is read from --device-config, '
                     'if no device_config found: a new device is registered '
                     'using a unique id and a new device config is saved')))
@click.option('--device-config', show_default=True,
              metavar='<device config>',
              default=os.path.join(
                  click.get_app_dir('googlesamples-assistant'),
                  'device_config.json'),
              help='Path to save and restore the device configuration')
@click.option('--lang', show_default=True,
              metavar='<language code>',
              default='ko-kr',
              help='Language code of the Assistant')
@click.option('--display', is_flag=True, default=False,
              help='Enable visual display of Assistant responses in HTML.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Verbose logging.')
@click.option('--input-audio-file', '-i',
              metavar='<input file>',
              help='Path to input audio file. '
              'If missing, uses audio capture')
@click.option('--output-audio-file', '-o',
              metavar='<output file>',
              help='Path to output audio file. '
              'If missing, uses audio playback')
@click.option('--audio-sample-rate',
              default=audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE,
              metavar='<audio sample rate>', show_default=True,
              help='Audio sample rate in hertz.')
@click.option('--audio-sample-width',
              default=audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH,
              metavar='<audio sample width>', show_default=True,
              help='Audio sample width in bytes.')
@click.option('--audio-iter-size',
              default=audio_helpers.DEFAULT_AUDIO_ITER_SIZE,
              metavar='<audio iter size>', show_default=True,
              help='Size of each read during audio stream iteration in bytes.')
@click.option('--audio-block-size',
              default=audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE,
              metavar='<audio block size>', show_default=True,
              help=('Block size in bytes for each audio device '
                    'read and write operation.'))
@click.option('--audio-flush-size',
              default=audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE,
              metavar='<audio flush size>', show_default=True,
              help=('Size of silence data in bytes written '
                    'during flush operation'))
@click.option('--grpc-deadline', default=DEFAULT_GRPC_DEADLINE,
              metavar='<grpc deadline>', show_default=True,
              help='gRPC deadline in seconds')
@click.option('--once', default=False, is_flag=True,
              help='Force termination after a single conversation.')


def main(api_endpoint, credentials, project_id,
         device_model_id, device_id, device_config,
         lang, display, verbose,
         input_audio_file, output_audio_file,
         audio_sample_rate, audio_sample_width,
         audio_iter_size, audio_block_size, audio_flush_size,
         grpc_deadline, once, *args, **kwargs):
    """Samples for the Google Assistant API.

    Examples:
      Run the sample with microphone input and speaker output:

        $ python -m googlesamples.assistant

      Run the sample with file input and speaker output:

        $ python -m googlesamples.assistant -i <input file>

      Run the sample with file input and output:

        $ python -m googlesamples.assistant -i <input file> -o <output file>
    """

    # Setup logging.
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    # Load OAuth 2.0 credentials.
    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials: %s', e)
        logging.error('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')
        sys.exit(-1)

    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    # Configure audio source and sink.
    audio_device = None
    if input_audio_file:
        audio_source = audio_helpers.WaveSource(
            open(input_audio_file, 'rb'),
            sample_rate=audio_sample_rate,
            sample_width=audio_sample_width
        )
    else:
        audio_source = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_sample_rate,
                sample_width=audio_sample_width,
                block_size=audio_block_size,
                flush_size=audio_flush_size
            )
        )
    if output_audio_file:
        audio_sink = audio_helpers.WaveSink(
            open(output_audio_file, 'wb'),
            sample_rate=audio_sample_rate,
            sample_width=audio_sample_width
        )
    else:
        audio_sink = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_sample_rate,
                sample_width=audio_sample_width,
                block_size=audio_block_size,
                flush_size=audio_flush_size
            )
        )
    # Create conversation stream with the given audio source and sink.
    conversation_stream = audio_helpers.ConversationStream(
        source=audio_source,
        sink=audio_sink,
        iter_size=audio_iter_size,
        sample_width=audio_sample_width,
    )

    if not device_id or not device_model_id:
        try:
            with open(device_config) as f:
                device = json.load(f)
                device_id = device['id']
                device_model_id = device['model_id']
                logging.info("Using device model %s and device id %s",
                             device_model_id,
                             device_id)
        except Exception as e:
            logging.warning('Device config not found: %s' % e)
            logging.info('Registering device')
            if not device_model_id:
                logging.error('Option --device-model-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            if not project_id:
                logging.error('Option --project-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            device_base_url = (
                'https://%s/v1alpha2/projects/%s/devices' % (api_endpoint,
                                                             project_id)
            )
            device_id = str(uuid.uuid1())
            payload = {
                'id': device_id,
                'model_id': device_model_id,
                'client_type': 'SDK_SERVICE'
            }
            session = google.auth.transport.requests.AuthorizedSession(
                credentials
            )
            r = session.post(device_base_url, data=json.dumps(payload))
            if r.status_code != 200:
                logging.error('Failed to register device: %s', r.text)
                sys.exit(-1)
            logging.info('Device registered: %s', device_id)
            pathlib.Path(os.path.dirname(device_config)).mkdir(exist_ok=True)
            with open(device_config, 'w') as f:
                json.dump(payload, f)

    device_handler = device_helpers.DeviceRequestHandler(device_id)

    @device_handler.command('action.devices.commands.OnOff')
    def onoff(on):
        if on:
            logging.info('Turning device on')
        else:
            logging.info('Turning device off')

    @device_handler.command('com.example.commands.BlinkLight')
    def blink(speed, number):
        logging.info('Blinking device %s times.'% number)
        delay = 1
        if speed == "SLOWLY":
            delay = 2
        elif speed == "QUICKLY":
            delay = 0.5
        for i in range(int(number)):
            logging.info('Device is blinking.')
            time.sleep(delay)
    
    def tts(text,lang='ko'):
        if lang == None:
            speech = gTTS(text=text)
        else:
            speech = gTTS(text=text,lang=lang)
        speech.save('tmp.mp3')
        os.system("omxplayer tmp.mp3")
        os.remove('tmp.mp3')

    def stt(commands=None,is_respon=False):
        # voice recognition/respone.*******
        continue_conversation, stt_tmp = assistant.assist(commands=commands,is_respon=is_respon)
        
        wait_for_user_trigger = not continue_conversation
        
        #if once and (not continue_conversation):            
        #    break
        
        text = stt_tmp

        return text


    with SampleAssistant(lang, device_model_id, device_id,
                         conversation_stream, display,
                         grpc_channel, grpc_deadline,
                         device_handler) as assistant:
        if input_audio_file or output_audio_file:
            assistant.assist()
            return
        
        wait_for_user_trigger = not once

        select = ['컨트롤','교육']
        control = ['초음파','추적','불빛','명령','꺼']
        yn = ['네','아니']
        move=['앞으로','뒤로','오른쪽','왼쪽']
        
        first = True
        more = False

        #dc_ultra = m.ultra_sonic()
        module = m.mode()

        while True:
            if first == True:
                tts("컨트롤모드와 교육모드 중에 선택해주세요 ,.,.,.")
                first = False

            text = stt(select,is_respon=True)
            print("[INFO] answer : ",text)   

            if select[0] in text:
                print('동작 모드 ')
                tts('동작모드 입니다....   ')

                while True:

                    if more == True:
                        tts("동작모드를 더 하실껀가요   ")

                        text = stt(is_respon=False)

                        if yn[0] in text:
                            more = False
                            tts('다시 시작할게요   ')
                        if yn[1] in text:
                            more = False
                            first = True
                            break

                    text = stt(is_respon=False)
                    print("[INFO] answer : ",text) 
                     
                    if control[0] in text:
                        print("초음파 모드")
                        tts('초음파 모드 입니다   ')
                        sel = random.randrange(2)
                        
                        if sel == 0:
                            print('1')
                            module.avoid()
                        else:
                            print('2')
                            module.avoid2()

                        tts("초음파 모드가 끝났어요   ")
                        
                        more = True

                            
                    elif control[1] in text:
                        print('추적 모드')
                        tts('추적 모드 입니다   ')
                        module.tracking()
                        
                        tts("추적 모드가 끝났어요   ")

                        more = True

                    elif control[2] in text:
                        print('불빛 모드')
                        tts('블빛 모드 입니다   ')
                        module.servo_led()

                        tts("붗빛 모드가 끝났어요 ")
                
                        more = True

                    elif control[3] in text:
                        print('명령모드')
                        tts('명령 모드 입니다   ')
                        
                        try:
                            start = time.time()
                            while True:
                                if time.time() - start > 60:
                                    break
                                text = stt(commands=move,is_respon=False)
                                print(text) 
                                if move[0] in text:
                                    #if module.distance() > 80:
                                    module.go(100,100)
                                    sleep(2)
                                    module.stop()
                                elif move[1] in text:
                                    module.back(100,100)
                                    sleep(2)
                                    module.stop()
                                elif move[2] in text:
                                    module.spin_right(100,100)
                                    sleep(3)
                                    module.stop()
                                elif move[3] in text:
                                    module.spin_left(100,100)
                                    sleep(3) 
                                    module.stop()

                        except KeyboardInterrupt:
                            module.stop()
                        
                        module.stop()
                        tts("명령모드가 끝났어요    ")

                        more = True
                    
                    elif control[4] in text:
                        tts("끝낼게요    ")
                        first = True
                        break
                        
            elif select[1] in text:
                #DB Setting
                host = '192.168.0.8'
                user = 'root'
                dbname = 'Education'
                password = '1234'
                ser = 1
                name = 'LEE'
                e = Education(host, user, dbname, password, ser, name)
                conn, cur = e.connection()
                e.dbclean(conn, cur)
                tts("교육모드 입니다.   ")
                
                count = 0
                stage = 0

                while True:
                    distance = module.distance()
                    
                    if distance < 50:
                        count += 1

                    if count > 100:
                        count = 0

                        tts("반가워요 제가 동화를 들려드릴게요  ")
                        sleep(1)
                        os.system("omxplayer ~/workspace/Raspi_google_robot/stt/ka_01.mp3") 

                        tts("동화가 끝났어요 재미있으셨나요  ")
                        sleep(1)

                        while True:
                            text = stt(is_respon=False)
                            e.isfun(conn, cur, text)
                            if yn[0] in text:
                                tts("고마워요 다음에 또 들려줄게요  ")
                                break
                            elif yn[1] in text:
                                tts("나중에는 더 재미있는 이야기를 들려줄게요  ")
                                break
                        e.search_isfun(conn, cur)
                        tts("우리 같이 숫자 공부해요  ")
                        sleep(1)
                        tts("일 더하기 이는 무엇일까요  ")
                        
                        life = 5
                        math_pt = 100
                        while True:
                            text = stt(is_respon=False)
                            print(text)

                            if '3' in text:
                                tts("정답이에요 축하해요  ")
                                break
                            elif not text:
                                pass
                            else:
                                tts("틀렸어요 다시한번 말해주세요  ")
                                life -= 1
                                math_pt -= 5
                                if life == 0:
                                    tts("코인을 다썼어요 아쉽네요 다음 기회에 또 봐요  ")
                                    break
                        e.math(conn, cur, math_pt)
                        e.search_math(conn, cur)
                        time.sleep(1)
                        
                        tts("우리 같이 발음을 맞춰봐요  ")
                        
                        life = 5
                        english_pt = 100

                        quiz = 'orange'
                        
                        tts(quiz,lang=None)
                        
                        while True:
                            text = stt(is_respon=False)
                            print(text)

                            if '오렌지' in text:
                                tts("정답 이에요")
                                break
                            elif not text:
                                pass
                            else:
                                tts("틀렸어요 다시한번 말해주세요    ")
                                life -= 1
                                english_pt -= 5
                                if life == 0:
                                    tts("아쉽네요 다음 기회에 또 봐요     ")
                                    break
                        e.english(conn, cur, english_pt)        
                        e.search_english(conn, cur)
                        time.sleep(1)
                        
                        tts("교육모드가 끝났습니다.    ")
                        e.dbclose(conn, cur) 
                        first = True
                        break
            else:
                first = True
        m.clean()
            
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    main()
