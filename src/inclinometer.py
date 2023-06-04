import time
from math import atan2, degrees
import board
import adafruit_lsm303_accel


class Inclinometer:
    def __init__(self, i2c) -> None:
        self.sensor = adafruit_lsm303_accel.LSM303_Accel(i2c)

    def vector_2_degrees(self, x, y):
        angle = degrees(atan2(y, x)) - 90
        if angle < -180:
            angle += 360
        return angle

    def get_inclination(self):
        x, y, z = self.sensor.acceleration
        return self.vector_2_degrees(x, z), self.vector_2_degrees(y, z)


if __name__ == "__main__":
    i2c = board.I2C()
    inclinometer = Inclinometer(i2c)

    while True:
        angle_xz, angle_yz = inclinometer.get_inclination()
        print(
            "XZ angle = {:6.2f}deg   YZ angle = {:6.2f}deg".format(angle_xz, angle_yz)
        )
        time.sleep(0.2)
