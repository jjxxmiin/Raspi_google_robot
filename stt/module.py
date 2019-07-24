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

    def go(self,leftspeed,rightspeed):
        print("[INFO] DC Motor : GO")
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)

        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)
        
        self.pwm_1E.ChangeDutyCycle(leftspeed)
        self.pwm_2E.ChangeDutyCycle(rightspeed)
        
    def back(self,leftspeed,rightspeed):
        print("[INFO] DC Motor : BACK")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.HIGH)
        GPIO.output(self.Motor2E,GPIO.HIGH)

        self.pwm_1E.ChangeDutyCycle(leftspeed)
        self.pwm_2E.ChangeDutyCycle(rightspeed)

    def right(self,leftspeed,rightspeed):
        print("[INFO] DC Motor : RIGHT")
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)
        
        self.pwm_1E.ChangeDutyCycle(leftspeed)
        self.pwm_2E.ChangeDutyCycle(rightspeed)
    
    def left(self,leftspeed,rightspeed):
        print("[INFO] DC Motor : LEFT")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH) 
        
        self.pwm_1E.ChangeDutyCycle(leftspeed)
        self.pwm_2E.ChangeDutyCycle(rightspeed)

    def spin_left(self,leftspeed, rightspeed):
        print("[INFO] DC Motor : SPIN LEFT")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)
        
        self.pwm_1E.ChangeDutyCycle(leftspeed)
        self.pwm_2E.ChangeDutyCycle(rightspeed)
    
    def spin_right(self,leftspeed, rightspeed):
        print("[INFO] DC Motor : SPIN RIGHT")
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
      
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.HIGH)
        GPIO.output(self.Motor2E,GPIO.HIGH)
        
        self.pwm_1E.ChangeDutyCycle(leftspeed)
        self.pwm_2E.ChangeDutyCycle(rightspeed)
    
    def stop(self):
        print("[INFO] DC Motor : GO")
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

class Track():
    def __init__(self):
        self.LeftPin1 = 3
        self.LeftPin2 = 5
        self.RightPin1 = 4
        self.RightPin2 = 18
        self.dc = dcmotor()

        GPIO.setup(self.LeftPin1, GPIO.IN)
        GPIO.setup(self.LeftPin2, GPIO.IN)
        GPIO.setup(self.RightPin1, GPIO.IN)
        GPIO.setup(self.RightPin2, GPIO.IN)
        
    def start(self):
        dc = self.dc
        LeftValue1  = GPIO.input(self.LeftPin1)
        LeftValue2  = GPIO.input(self.LeftPin2)
        RightValue1 = GPIO.input(self.RightPin1)
        RightValue2 = GPIO.input(self.RightPin2)

        if (LeftValue1 == False or LeftValue2 == False) and  RightValue2 == False:
            dc.spin_right(35, 35)
            time.sleep(0.08)
 
        elif LeftValue1 == False and (RightValue1 == False or  RightValue2 == False):
            dc.spin_left(35, 35)
            time.sleep(0.08)
        
        elif LeftValue1 == False:
            dc.spin_left(35, 35)
     
        elif RightValue2 == False:
            dc.spin_right(35, 35)
   
        elif LeftValue2 == False and RightValue1 == True:
            dc.left(0,40)
    
        elif LeftValue2 == True and RightValue1 == False:
            dc.right(40, 0)
   
        elif LeftValue2 == False and RightValue1 == False:
            dc.go(50, 50)
        
