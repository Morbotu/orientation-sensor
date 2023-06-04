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
        return -angle

    def __get_angle_xz(self):
        return self.vector_2_degrees(self.x, self.z)

    def __get_angle_yz(self):
        return self.vector_2_degrees(self.y, self.z)

    def measure(self):
        self.x, self.y, self.z = self.sensor.acceleration

    angle_xz = property(__get_angle_xz)
    angle_yz = property(__get_angle_yz)


if __name__ == "__main__":
    i2c = board.I2C()
    inclinometer = Inclinometer(i2c)

    while True:
        inclinometer.measure()
        angle_xz = inclinometer.angle_xz
        angle_yz = inclinometer.angle_yz
        print(
            "XZ angle = {:6.2f}deg   YZ angle = {:6.2f}deg".format(angle_xz, angle_yz)
        )
        time.sleep(0.2)
