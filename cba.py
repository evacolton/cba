#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance via UltrasonicRanging sensor
# auther      : Eva Colton
# modification: 9/3/21
########################################################################
import RPi.GPIO as GPIO
import time

ledpin = 11
trigPin = 16
echoPin = 18
MAX_DISTANCE = 200   # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar():     # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      # make trigPin output 10us HIGH level
    time.sleep(0.00001)     # 10us
    GPIO.output(trigPin,GPIO.LOW) # make trigPin output LOW level
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s
    return distance

def setup():
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
    GPIO.setup(ledpin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(ledpin, GPIO.LOW) 

def loop():
    womp = 0
    while(True):

        distance = getSonar() # get distances
        if 5 < distance < 10:
            print (f"The distance is : {distance:.2f} cm. Womp is {womp}")
            womp = womp + 1
        else :
            womp = 0
        time.sleep(.1)

        if womp == 10:
            GPIO.output(ledpin, GPIO.HIGH)
            print("womp womp")
            time.sleep(.1)
            GPIO.output(ledpin, GPIO.LOW)
            womp = 0






if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        GPIO.cleanup()         # release GPIO resource



