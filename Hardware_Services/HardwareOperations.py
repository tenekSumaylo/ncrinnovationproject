import RPi.GPIO as GPIO
#import asyncio
import time
from time import sleep
from threading import Thread

class HardwareActions:
	def __init__(self):
		self.solenoid_one = 21
		self.pulse = 24
		self.direction = 27 
		self.enable = 22
		GPIO.setmode( GPIO.BCM )
		GPIO.setup( self.solenoid_one, GPIO.OUT ) 
		GPIO.setup(self.pulse, GPIO.OUT)
		GPIO.setup(self.direction, GPIO.OUT)
		GPIO.setup(self.enable, GPIO.OUT)
		
	def activate_solenoid_one(self):
		GPIO.output( self.solenoid_one, GPIO.HIGH )
		
	def deactivate_solenoid_one(self):
		GPIO.output( self.solenoid_one, GPIO.LOW )
		
	def employee_verified(self):
		self.activate_solenoid_one()
		sleep(1.5)
		self.deactivate_solenoid_one()
	
	def solenoid_on(self):
		Thread(target=self.employee_verified, daemon=True).start()
		
	def activate_stepper(self):
		GPIO.output(self.enable, GPIO.HIGH)

		sleep(.5) 
		GPIO.output(self.direction, GPIO.LOW)

		for x in range(300): 
			GPIO.output(self.pulse, GPIO.HIGH)
			sleep(0.0003)
			GPIO.output(self.pulse, GPIO.LOW)
			sleep(0.0003)
		sleep(.5) 
    
	def deactivate_stepper(self):
		GPIO.output(self.direction, GPIO.HIGH)
		for y in range(300):
			GPIO.output(self.pulse, GPIO.HIGH)
			sleep(0.0003)
			GPIO.output(self.pulse, GPIO.LOW)
			sleep(0.0003)
		GPIO.output(self.enable, GPIO.LOW)
		sleep(.5)
		
	def stepper_on(self):
		Thread(target = self.activate_stepper, daemon=True).start()
	def stepper_off(self):
		Thread(target = self.deactivate_stepper, daemon=True).start()
		
	def toolbox_open(self):
		self.activate_stepper()
		sleep(5)
		self.deactivate_stepper()
	
	def gpio_clean_all(self):
		used_pins = [21, 24, 27]
		# ~ 21 = Solenoid
		# ~ 24 = pulse signal
		# ~ 27 = Direction signal
		# ~ Ignore Enable pin to keep it free wheeling when not used
		for pin in used_pins:
			GPIO.cleanup(used_pins)	
		print( "Successfully Cleaned GPIOs" ) 

