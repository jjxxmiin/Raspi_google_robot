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

# requirement
- google assistant library [[참고](https://jjeamin.github.io/pi/2019/07/09/googleapi/)]

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

motor_test.py

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

tts_test.py

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
