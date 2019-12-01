from picamera import PiCamera, Color
from time import sleep
import RPi.GPIO as GPIO
import time
import random as rand
import time
from time import sleep
import os
import datetime as dt
import time
import random

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers


camera = PiCamera()
camera.resolution = (2592, 1944)
camera.led = False

off = GPIO.HIGH
on = GPIO.LOW
theAlmConstant = 1.5
drunkModifier = 2


PORT0 = 4
PORT1 = 17
PORT2 = 22
PORT3 = 27

ledPin = 13
buttonPin = 6

GPIO.setup(PORT0, GPIO.OUT)
GPIO.setup(PORT1, GPIO.OUT)
GPIO.setup(PORT2, GPIO.OUT)
GPIO.setup(PORT3, GPIO.OUT)

GPIO.output(PORT0,off) # out
GPIO.output(PORT1,off) # out
GPIO.output(PORT2,off) # out
GPIO.output(PORT3,off) # out

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def take_picture():
    GPIO.output(PORT3,on) # out
    camera.annotate_background = Color('black')
    text = "Brygg paa nybygd brygge\n%s"%dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.annotate_text = text
    camera.annotate_text_size = 90
    camera.capture('/home/pi/pictures/%s.jpg'%int(time.time()))
    GPIO.output(ledPin, GPIO.HIGH)
    GPIO.output(PORT3,off) # out
    
boozes = [PORT0,PORT1]
    
while True:
    buttonState = GPIO.input(buttonPin)
    if buttonState == False:
        
        take_picture()
        
        random.shuffle(boozes)
        GPIO.output(boozes[0],on) # out
        sleep(1.7)
        GPIO.output(boozes[0],off) # out
        
        take_picture()
        

    else:
        
        
        GPIO.output(ledPin, GPIO.LOW)


