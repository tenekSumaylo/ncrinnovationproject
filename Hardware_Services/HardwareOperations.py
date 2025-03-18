import RPi.GPIO as GPIO
import asyncio
import time

class HardwareActions:
	def __init__(self):
		self.solenoid_one = 6
		GPIO.cleanup()
		GPIO.setmode( GPIO.BCM )
		GPIO.setup( self.solenoid_one, GPIO.OUT ) 
		
	def activate_solenoid_one(self):
		GPIO.output( self.solenoid_one, GPIO.HIGH )
		
	def deactivate_solenoid_one(self):
		GPIO.output( self.solenoid_one, GPIO.LOW )
		
	async def employee_verified(self):
		self.activate_solenoid_one()
		await asyncio.sleep(1.5)
		self.deactivate_solenoid_one()
	
	def gpio_clean_all(self):
		GPIO.cleanup()	
		print( "Successfully Cleaned GPIOs" ) 
