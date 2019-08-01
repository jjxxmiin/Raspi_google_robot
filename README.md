---
layout: post
title:  "Google Sample Code 수정"
summary: "Google Sample Code 살펴보고 STT부분 찾아서 이용하기"
date:   2019-07-13 13:00 -0400
categories: pi
---

# Dependency
- 라즈베리파이 3B+
- 마이크, 스피커
- 모듈 : dc motor, ultra sonic, servo motor, led
- 부록 : 카메라, 블루투스

# requirement
- google assistant library 
- gTTS

# 원리

```
google assistant ---> 동작 모드 --->   초음파       ---> 초음파 모드 실행  ---> 동작모드 재실행 여부 ---> 예    : 동작모드
                 |                 |   불빛        ---> 불빛 모드 실행                            ---> 아니오 : 처음으로
                 |                 |   추적        ---> 추적 모드 실행
                 |                 |   명령        ---> 명령 모드 실행
                 |                    
                 ---> 교육 모드 ---> 동화 들려주기 ---> 문제 풀기        ---> 단어 말하기
```

---

# google assistant sample

push to talk에서 STT하는 부분을 찾아서 값을 가져오게 하기 (**google assistant 기능과 stt 기능을 전부다 이용하기 위함**)

---

# Module

- ultra sonic
- servo motor
- led
- dc motor

---

# TTS

```
pip install gTTS
```

```python
from gtts import gTTS
tts = gTTS('안녕', lang='ko')
tts.save('hello.mp3')
```

---

# 사용법

1. google assistant libary 설치 : [[참고](https://jjeamin.github.io/pi/2019/07/09/googleapi/)]

2. glt clone

```
git clone https://github.com/jjeamin/Raspi_google_robot.git
```

motule_new.py에서 pin number를 조정해주면 된다.

3. 실행

```
python backup.py --project-id <your project id> --device-model-id <your device id>
```

4. 시나리오 수정하기

:rage2: **보완해줘야할 사항**

- google assistant 이용량 제한
- tts 부분은 직접 녹음해야한다

---

# mode

- 동작용
- 교육용

---

# 동작용

동작을 진행하는 모드

## 추적

라인을 Tracking 하는 Mode

## 불빛

LED가 색상 별로 나오는 Mode

## 초음파

초음파 센서 + dc모터를 결합해 앞에 장애물이 있으면 피해가는 Mode(모터의 속도 등을 고려해봤는데 잘 동작이 안된다.. 이유를 아직 파악못함)

## 명령

```
앞으로가
뒤로가
왼쪽으로가
오른쪽으로가
```

---

# 교육용

교육을 진행하는 모드

## 동화 들려주기

일정시간 앞에 있으면 동화를 들려주는 것으로 시작한다. 그 후에 재미있었는지 없었는지에 대한 대답을 DB에 저장되는 단계

## 문제 풀기

단순한 계산 문제를 풀수 있도록 하고 정답이 맞으면 그에 해당하는 점수가 DB에 저장되는 단계

## 단어 발음 말하기

단어의 발음을 맞추어 보면서 단어의 발음이 정확하면 그에 해당하는 점수가 DB에 저장되는 단계

---

# 부록 : MJPEG

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git cmake libjpeg-dev imagemagick -y
```

```
cd mjpg-streamer/mjpg-streamer-experimental/
make CMAKE_BUILD_TYPE=Debug
sudo make install
```

```
./start.sh
```

```
127.0.0.1:8080 접속
```

# 부록 : 블루투스 설정

시리얼 통신을 이용해서 블루투스를 이용하기 위해서는 기존의 블루투스의 기능을 없애줘야 하기 때문에 없애고 시작을 하기로 하자

```
sudo raspi-config
```

`Interfacing Options` -> `Serial Port Enable`, `Serial Console Disable`

```
sudo vi /boot/config.txt
```

맨아래로 가서 아래 코드 삽입

```
enable_uart=1
#disable bluetooth
dtoverlay=pi3-disable-bt
```

저장한 뒤에 아래 명령어를 사용하고 재부팅

```
sudo systemctl disable hciuart
```

python 코드 사용법

```python
import serial

ser = serial.Serial("/dev/ttyAMA0", "9600")
```

통신속도 확인

```
sudo stty -F /dev/ttyAMA0
```
