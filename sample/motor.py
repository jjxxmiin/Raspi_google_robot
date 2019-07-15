import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

servo = 4

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 20
Motor2B = 21
Motor2E = 22

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

GPIO.setup(servo,GPIO.OUT)

p1 = GPIO.PWM(Motor1E,100)
p2 = GPIO.PWM(Motor2E,100)
servo_p = GPIO.PWM(servo,50)

servo_p.start(0)

n_speed = 5

def left_tire(mode):
	if mode == 0:
		GPIO.output(Motor1A,GPIO.HIGH)
        	GPIO.output(Motor1B,GPIO.LOW)
        	GPIO.output(Motor1E,GPIO.HIGH)
		left_setSpeed(4)
	elif mode == 1:
		GPIO.output(Motor1A,GPIO.LOW)
		GPIO.output(Motor1B,GPIO.HIGH)
		GPIO.output(Motor1E,GPIO.HIGH)
		left_setSpeed(4)
	elif mode == -1:
		GPIO.output(Motor1E,GPIO.LOW)	
		left_setSpeed(0)
	else:
		print('left_tire mode error')

def right_tire(mode):
	if mode == 0:
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.HIGH)
		right_setSpeed(4)
        elif mode == 1:
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                GPIO.output(Motor2E,GPIO.HIGH)
		right_setSpeed(4)
	elif mode == -1:
		GPIO.output(Motor2E,GPIO.LOW)
		right_setSpeed(0)
	else:
		print('right_tire mode error')

def go():
	right_tire(1)
	left_tire(1)	

def back():
	right_tire(0)
	left_tire(0)

def right():
	left_tire(1)
	right_tire(-1)

def left():
	right_tire(1)
	left_tire(-1)
	
def stop():
	GPIO.output(Motor1E,GPIO.LOW)
	GPIO.output(Motor2E,GPIO.LOW)
	setSpeed(0,0)

def go_left():
	right_tire(1)
	left_tire(1)
	setSpeed(5,3)

def go_right():
	right_tire(1)
	left_tire(1)
	setSpeed(3,5)
	
def back_left():
	right_tire(0)
	left_tire(0)
	setSpeed(5,3)
	
def back_right():
	right_tire(0)
	left_tire(0)
	setSpeed(3,5)
	
def left_setSpeed(speed):
	p1.start(0)
	p1.ChangeDutyCycle(speed*10)

def right_setSpeed(speed):
        p2.start(0)
        p2.ChangeDutyCycle(speed*10)

def setSpeed(left_speed,right_speed):
	p1.start(0)
	p2.start(0)

	p1.ChangeDutyCycle(left_speed*10)
	p2.ChangeDutyCycle(right_speed*10)

def setServo(degree):	
	servo_p.ChangeDutyCycle(degree)

def clean():
	GPIO.cleanup()

'''
go()
sleep(2)
back()
sleep(2)
'''
