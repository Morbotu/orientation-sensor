import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin=16):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm=GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()
    
    def setAngle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)

if __name__ == "__main__":
    servo = Servo()
    while True:
        angle = input("Angle: ")
        if angle == "stop":
            break
        servo.setAngle(int(angle))

    del servo