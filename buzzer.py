#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

BeepPin = 11    # pin11

def setup():
	GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
	GPIO.setup(BeepPin, GPIO.OUT)   # Set BeepPin's mode is output
	GPIO.output(BeepPin, GPIO.HIGH) # Set BeepPin high(+3.3V) to off beep


if __name__ == '__main__':     # Program start from here
	
	setup()
	GPIO.output(BeepPin, GPIO.LOW)
	time.sleep(0.1)
	GPIO.output(BeepPin, GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(BeepPin, GPIO.LOW)
	time.sleep(0.1)
	GPIO.output(BeepPin, GPIO.HIGH)
	time.sleep(0.1)    
	GPIO.cleanup()    
	
