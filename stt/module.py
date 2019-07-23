import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setwarnings(False)

class dcmotor():
    def __init__(self):
        self.Motor1A = 20
        self.Motor1B = 21
        self.Motor1E = 16

        self.Motor2A = 19
        self.Motor2B = 26
        self.Motor2E = 13	

        GPIO.setup(self.Motor1A,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.Motor1B,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.Motor1E,GPIO.OUT,initial=GPIO.HIGH)
                 
        GPIO.setup(self.Motor2A,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.Motor2B,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.Motor2E,GPIO.OUT,initial=GPIO.HIGH)

        self.pwm_1E = GPIO.PWM(self.Motor1E, 2000)
        self.pwm_2E = GPIO.PWM(self.Motor2E, 2000)

# 1 ~ 100
    def setspeed(self,speed):
        self.pwm_1E.start(speed)
        self.pwm_2E.start(speed)

    def go(self):
        print("[INFO]DC Motor : GO")
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)

        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)

    def back(self):
        print("[INFO]DC Motor : BACK")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.HIGH)
        GPIO.output(self.Motor2E,GPIO.HIGH)

    def right(self):
        print("[INFO]DC Motor : RIGHT")
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)
    
    def left(self):
        print("[INFO]DC Motor : LEFT")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH) 

    def stop(self):
        print("[INFO]DC Motor : GO")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.LOW)

    def clean(self):
        GPIO.cleanup()

class ultra_sonic():
    def __init__(self):
        self.EchoPin = 0
        self.TrigPin = 1
        
        GPIO.setup(self.EchoPin,GPIO.IN)
        GPIO.setup(self.TrigPin,GPIO.OUT)

    def distance(self):
        GPIO.output(self.TrigPin,GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin,GPIO.LOW)
        while not GPIO.input(self.EchoPin):
            pass
        t1 = time.time()
        while GPIO.input(self.EchoPin):
            pass
        t2 = time.time()
        
        dis = ((t2 - t1) * 340 / 2) * 100

        time.sleep(0.01)    

        return dis
 
class LED():
    def __init__(self):
        self.LED_R = 22
        self.LED_G = 27
        self.LED_B = 24
        
        GPIO.setup(self.LED_R, GPIO.OUT)
        GPIO.setup(self.LED_G, GPIO.OUT)
        GPIO.setup(self.LED_B, GPIO.OUT)

    def red(self):
        GPIO.output(self.LED_R, GPIO.HIGH)
        GPIO.output(self.LED_G, GPIO.LOW)
        GPIO.output(self.LED_B, GPIO.LOW)
        
    def blue(self):
        GPIO.output(self.LED_R, GPIO.LOW)
        GPIO.output(self.LED_G, GPIO.LOW)
        GPIO.output(self.LED_B, GPIO.HIGH)   
         
    def green(self):
        GPIO.output(self.LED_R, GPIO.LOW)
        GPIO.output(self.LED_G, GPIO.HIGH)
        GPIO.output(self.LED_B, GPIO.LOW)   
         
    def rb(self):
        GPIO.output(self.LED_R, GPIO.HIGH)
        GPIO.output(self.LED_G, GPIO.LOW)
        GPIO.output(self.LED_B, GPIO.HIGH)
        
    def rg(self):
        GPIO.output(self.LED_R, GPIO.HIGH)
        GPIO.output(self.LED_G, GPIO.HIGH)
        GPIO.output(self.LED_B, GPIO.LOW)
        
    def bg(self):
        GPIO.output(self.LED_R, GPIO.LOW)
        GPIO.output(self.LED_G, GPIO.HIGH)
        GPIO.output(self.LED_B, GPIO.HIGH)
        
    def all(self):
        GPIO.output(self.LED_R, GPIO.HIGH)
        GPIO.output(self.LED_G, GPIO.HIGH)
        GPIO.output(self.LED_B, GPIO.HIGH)
        
    def off(self):
        GPIO.output(self.LED_R, GPIO.LOW)
        GPIO.output(self.LED_G, GPIO.LOW)
        GPIO.output(self.LED_B, GPIO.LOW)
        
class servo():
   def __init__(self):
        self.ServoFrontPin = 23
        ServoUpDownPin = 9;
        ServoLeftRightPin = 11;
        GPIO.setup(self.ServoUpDownPin, GPIO.OUT)
        GPIO.setup(self.ServoLeftRightPin, GPIO.OUT)
        GPIO.setup(self.ServoFrontPin, GPIO.OUT)
                
        pwm_servo = GPIO.PWM(self.ServoPin, 50)
        pwm_servo.start(0)
        
        
