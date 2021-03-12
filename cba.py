#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance via UltrasonicRanging sensor
# auther      : Eva Colton
# modification: 9/3/21
########################################################################
import RPi.GPIO as GPIO
import time

servoPin = 11
trigPin = 16
echoPin = 18
OFFSE_DUTY = 0.5                     # define pulse offset of servo
SERVO_MIN_DUTY = 2.5 + OFFSE_DUTY      # define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5 + OFFSE_DUTY     #define pulse duty cycle for maximum angle of servo
MAX_DISTANCE = 200   # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def map( value, fromLow, fromHigh, toLow, toHigh): # map a value from one range to another range
    
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow # Set initial Duty Cycle to 0

def servoWrite(angle): # make the servo rotate to specific angle, 0-180
    if(angle<0):
        angle = 0
    elif(angle > 180):
        angle = 180
    p.ChangeDutyCycle(map(angle,0,180,SERVO_MIN_DUTY,SERVO_MAX_DUTY)) # map the angle to duty cycle and output it

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
    global p
    GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode
    GPIO.setup(servoPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(servoPin, GPIO.LOW)

    p = GPIO.PWM(servoPin, 50) # set Frequece to 50Hz
    p.start(0)


def loop():
    print(f'Starting loop ...')
    womp = 0
    while(True):
        distance = getSonar() # get distances
        if 3 < distance < 10:
            print (f"The distance is : {distance:.2f} cm. Womp is {womp}")
            womp = womp + 1
        else :
            womp = 0
        time.sleep(.1)

        if womp == 7:
           for dc in range(0, 181, 1): # make servo rotate from 0 to 180 deg
               servoWrite(dc) # Write dc value to servo
               time.sleep(0.001)
           time.sleep(0.2)
           for dc in range(180, -1, -1): # make servo rotate from 180 to 0 deg
                servoWrite(dc)
                time.sleep(0.001)
           time.sleep(0.2)
           womp = 0


if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        GPIO.cleanup()         # release GPIO resource



