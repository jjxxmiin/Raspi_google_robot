import RPi.GPIO as GPIO
import time

EchoPin = 0
TrigPin = 1

GPIO.setmode(GPIO.BCM)

GPIO.setup(EchoPin,GPIO.IN)
GPIO.setup(TrigPin,GPIO.OUT)

def Distance_test():
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()

    distance = ((t2-t1)*340/2)*100

    print("distance is %d" % distance)
    
    time.sleep(0.01)
    
    return distance

while True:
    Distance_test()
