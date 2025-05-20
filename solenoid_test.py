import RPi.GPIO as GPIO
import time

# Setup
RELAY_PIN = 21

GPIO.setmode(GPIO.BCM)        # Use BCM numbering
GPIO.setup(RELAY_PIN, GPIO.OUT)

print("Starting solenoid test. Press CTRL+C to stop.")

try:
    while True:
        print("Solenoid OFF")
        GPIO.output(RELAY_PIN, GPIO.LOW)  # LOW for active-low relay
        time.sleep(2)

        print("Solenoid ON")
        GPIO.output(RELAY_PIN, GPIO.HIGH) # HIGH to deactivate
        time.sleep(2)

except KeyboardInterrupt:
    print("Test stopped by user.")

finally:
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Ensure solenoid is off
    GPIO.cleanup()
