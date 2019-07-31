import RPi.GPIO as GPIO
from time import sleep
import time
GPIO.setwarnings(False)

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
        
    def led_off(self):
        GPIO.output(self.LED_R, GPIO.LOW)
        GPIO.output(self.LED_G, GPIO.LOW)
        GPIO.output(self.LED_B, GPIO.LOW)
    
    def event(self):
        try:
            while True:
                self.red()
                time.sleep(1)
                self.green()
                time.sleep(1)
                self.blue()
                time.sleep(1)
                self.rg()
                time.sleep(1)
                self.bg()
                time.sleep(1)
                self.rb()
                time.sleep(1)
                self.led_off()
                time.sleep(1)
        except KeyboardInterrupt:
            self.off()
            
    def color_light(self,pos):
        if pos > 150:
            self.red()
        elif pos > 125:
            self.blue()
        elif pos >100:
            self.green()
        elif pos > 75:
            self.rg()
        elif pos > 50:
            self.bg()
        elif pos > 25:
            self.rb()
        elif pos > 0:
            self.all()
        else :
            self.led_off()


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
        self.pwm_1E.start(0)
        self.pwm_2E.start(0)

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
        print("[INFO] DC Motor : STOP")
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.LOW)

class servo():
    def __init__(self):
        self.ServoFrontPin = 23
        self.ServoUpDownPin = 9;
        self.ServoLeftRightPin = 11;
        GPIO.setup(self.ServoUpDownPin, GPIO.OUT)
        GPIO.setup(self.ServoLeftRightPin, GPIO.OUT)
        GPIO.setup(self.ServoFrontPin, GPIO.OUT)
                
        self.pwm_servo = GPIO.PWM(self.ServoFrontPin, 50)
        self.pwm_servo.start(0)
        
    def appoint(self,pos):
        self.pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)    
        
    def servo_appointed_detection(self,pos):
        for i in range(18):
            self.appoint(pos)
            sleep(0.001)
            
    def servo_pulse(self,myangle):
        pulsewidth = (myangle * 11) + 500
        GPIO.output(self.ServoFrontPin, GPIO.HIGH)
        time.sleep(pulsewidth/1000000.0)
        GPIO.output(self.ServoFrontPin, GPIO.LOW)
        time.sleep(20.0/1000-pulsewidth/1000000.0)
            
    def servo_off(self):
        self.pwm_servo.ChangeDutyCycle(2.5 + 10 * 90/180)
        
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
        
class Track():
    def __init__(self):
        self.LeftPin1 = 3
        self.LeftPin2 = 5
        self.RightPin1 = 4
        self.RightPin2 = 18

        GPIO.setup(self.LeftPin1, GPIO.IN)
        GPIO.setup(self.LeftPin2, GPIO.IN)
        GPIO.setup(self.RightPin1, GPIO.IN)
        GPIO.setup(self.RightPin2, GPIO.IN)
        
    

def clean():
    GPIO.cleanup()

       
        
class mode(dcmotor,servo,Track,LED,ultra_sonic):
    def __init__(self):
        dcmotor.__init__(self)
        servo.__init__(self)
        Track.__init__(self)
        LED.__init__(self)
        ultra_sonic.__init__(self)
        
    def avoid(self):
        try:
            time.sleep(2)
            start = time.time()
            while True:
                if time.time() - start > 15:
                    break

                d = self.distance()
                
                if d > 50:
                    print(1)
                    self.go(60, 60)
                elif 30 <= d <= 50:
                    print(2)
                    self.go(55, 55)    
                elif d < 30:
                    print('3')
                    self.spin_right(50, 50)
                    time.sleep(0.7) 
                    self.stop()
                    time.sleep(0.01)
                    d = self.distance() 
                    if d >= 30:
                        self.go(60, 60)      
                    elif d < 30:
                        self.spin_left(50, 50)
                        time.sleep(1.4)  
                        self.stop()
                        time.sleep(0.01)
                        d = self.distance() 
                        if d >= 30:
                            self.go(60, 60)       
                        elif d < 30:
                            self.spin_left(50, 50)   
                            time.sleep(0.7)
                            self.stop()
                            time.sleep(0.01)
                
                print('[INFO] %d' % d)
            self.stop()
        except KeyboardInterrupt:
            self.stop()
            
    def avoid2(self):
        try:
            time.sleep(2)
            start = time.time()
            while True:
                if time.time() - start > 15:
                    break

                d = self.distance()
                if d > 50:
                    self.go(65, 65)
                elif 30 <= d <= 50:
                    self.go(55, 55)
                elif d < 30:
                    self.back(20, 20)
                    time.sleep(0.1)
                    self.stop()

                    self.servo_appointed_detection(0)
                    time.sleep(0.8)
                    rightdistance = self.distance()

                    self.servo_appointed_detection(180)
                    time.sleep(0.8)
                    leftdistance = self.distance()

                    self.servo_appointed_detection(90)
                    time.sleep(0.8)
                    frontdistance = self.distance()

                    if leftdistance < 30 and rightdistance < 30 and frontdistance < 30:
                            self.spin_right(55, 55)
                            time.sleep(0.58)
                    elif leftdistance >= rightdistance:
                            self.spin_left(55, 55)
                            time.sleep(0.28)
                    elif leftdistance <= rightdistance:
                            self.spin_right(55, 55)
                            time.sleep(0.28)

                print("[INFO] %d " % d)
            self.stop()
            
        except KeyboardInterrupt:
            self.stop()

    def tracking(self):
        try:
            start = time.time()
            while True:
                if time.time() - start > 10:
                    break
                    
                LeftValue1  = GPIO.input(self.LeftPin1)
                LeftValue2  = GPIO.input(self.LeftPin2)
                RightValue1 = GPIO.input(self.RightPin1)
                RightValue2 = GPIO.input(self.RightPin2)
                if (LeftValue1 == False or LeftValue2 == False) and  RightValue2 == False:
                    self.spin_right(35, 35)
                    time.sleep(0.08)
         
                elif LeftValue1 == False and (RightValue1 == False or  RightValue2 == False):
                    self.spin_left(35, 35)
                    time.sleep(0.08)
                
                elif LeftValue1 == False:
                    self.spin_left(35, 35)
             
                elif RightValue2 == False:
                    self.spin_right(35, 35)
           
                elif LeftValue2 == False and RightValue1 == True:
                    self.left(0,40)
            
                elif LeftValue2 == True and RightValue1 == False:
                    self.right(40, 0)
           
                elif LeftValue2 == False and RightValue1 == False:
                    self.go(50, 50)
            
        except KeyboardInterrupt:
            self.stop()
                
    def servo_led(self):
        try:
            start = time.time()
            self.appoint(90) 
            while True:
                if time.time() - start > 10:
                    break
                for pos in range(181):
                    self.appoint(pos)
                    self.color_light(pos)
                    time.sleep(0.01) 
                for pos in reversed(range(181)):
                    self.appoint(pos)
                    self.color_light(pos)
                    time.sleep(0.01)
                
        except KeyboardInterrupt:
            self.servo_off()
            self.led_off()
            
        self.servo_off()
        self.led_off()  
