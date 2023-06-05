import RPi.GPIO as GPIO
import time

pin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

pwm=GPIO.PWM(pin, 50)
pwm.start(0)

def setAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(pin, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(pin, False)
	pwm.ChangeDutyCycle(0)

while True:
	angle = input("Angle: ")
	if angle == "stop":
		break
	setAngle(int(angle))

pwm.stop()
GPIO.cleanup()