from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

PUL = 24  # Step
DIR = 27  # Dir, change direction when high or low
ENA = 22  # High for on state, Low for off state

# 3.3V is the 9th pin from top left going down
# Directly across 3.3v is pin 24
# Above 3.3v is pin 22 then pin 27

GPIO.setmode(GPIO.BCM)


GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)


durationFwd = 1200 # Duration of forward
durationBwd = 1200 # Duration of backward
# 5000 is 540 degrees-ish i think?


delay = 0.0003 # delay between pulses (higher meaning slower motor) just keep around 0.00001 to 0.0000001 


cycles = 3 # Times the whole program repeats itself
cyclecount = 0 # Where you want the repetition to start in cycle (Keep at 0 or not idk lmao)


def forward():
    GPIO.output(ENA, GPIO.HIGH)
    print("Motor On state Forwards")
    sleep(.5) 
    GPIO.output(DIR, GPIO.LOW)
    print("Direction: Forward")
    
    print("Moving Start")
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    print("Moving End")
    sleep(.5) 


def reverse():
    GPIO.output(DIR, GPIO.HIGH)
    print("Direction: Reverse")
    
    print("Moving Start")
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    print("Moving End")
    GPIO.output(ENA, GPIO.LOW)
    print("Motor Off Backwards State")
    sleep(.5) 
    return

while cyclecount < cycles:
    forward()
    reverse()
    cyclecount = (cyclecount + 1)
    print(f"Repetition #:{cyclecount}")
    
GPIO.output(ENA, GPIO.LOW)

