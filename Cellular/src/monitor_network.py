#!/usr/bin/python
import os
import RPi.GPIO as GPIO
import time, datetime
import urllib2

def check_connect_to_github():
    try:
        urllib2.urlopen('https://github.com/', timeout=5)
        return True
    except urllib2.URLError as err: 
        return False

def reset_network():
    GPIO.output(21, GPIO.LOW)
    time.sleep(1)
    GPIO.output(21, GPIO.HIGH)
    time.sleep(31)
    os.system('pppd call att-TNAG')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)

while 1:
    test_connected = check_connect_to_github()
    print datetime.datetime.utcnow().isoformat() + 'Z', test_connected
    if test_connected == False:
        reset_network()
    time.sleep(60)

