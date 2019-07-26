---
layout: post
title:  "Google Sample Code 수정"
summary: "Google Sample Code 살펴보고 STT부분 찾아서 이용하기"
date:   2019-07-13 13:00 -0400
categories: pi
---

# Dependency
- 라즈베리파이 3B+
- 마이크
- 스피커
- 블루투스 모듈(Serial)
- 카메라
- DC모터

# requirement
- google assistant library [[참고](https://jjeamin.github.io/pi/2019/07/09/googleapi/)]
- gTTS
- mjpg-stream

# 원리

```
google assistant ----(stt)---> motor 동작 ---(tts)----> response

+ 블루투스 무선조종
+ 카메라 스트리밍

```

---

# google sample

push to talk에서 STT하는 부분을 찾아서 값을 가져오게 하기

# pushtotalk.py

현재 Speech를 Text로 변환된 값을 가져오는 것은 가능하고 motor를 동작시키는 부분만 진행하면 될것이다.

---

# Motor

**motor_test.py**

```
go
back
stop
```

---

# TTS

```
pip install gTTS
```

**tts_test.py**

```python
from gtts import gTTS
tts = gTTS('안녕', lang='ko')
tts.save('hello.mp3')
```

---

# MJPEG

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

---

# mode

여러가지 mode

## problem

문제를 풀어야 하는 Mode

- 통과할 때 까지 진행
- 제한시간이 지나면 종료

## voca

단어의 발음을 맞추는 Mode

- 단어의 발음이 틀리면 재시도
- 통과할 때 까지 진행
- 제한시간이 지나면 종료

## story

시간마다 이야기를 들려주는 Mode

- `crontab`을 이용해서 설정 시간마다 이야기를 들려줌

## google

구글 어시스턴트 Mode

## move

명령에 따라 움직이는 Mode

```
앞으로가
왼쪽으로가
오른쪽으로가
뒤로가
```

## line

라인을 Tracking 하는 Mode

## avoid

초음파 센서 + dc모터 동작 Mode

## avoid2

초음파 센서 + dc모터 + servo모터 동작 Mode

## led

LED가 색상 별로 나오는 Mode
