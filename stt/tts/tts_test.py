from gtts import gTTS
import os 
text = "앞으로 갈게요."

tts = gTTS(text=text, lang='ko')
tts.save("temp.mp3")
os.system("omxplayer temp.mp3")
os.remove("temp.mp3")
