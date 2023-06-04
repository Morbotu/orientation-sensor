import time
import math
import board
import adafruit_lis2mdl
import os

class Compass:
    def __init__(self, i2c) -> None:
        self.sensor = adafruit_lis2mdl.LIS2MDL(i2c)
        self.calibrate() # [[-37.05, 122.69999999999999], [-71.1, 49.05], [-117.3, 27.15]]
        self.magnetic_values = None
    
    def __get_normalized_values(self):
        values = [0, 0, 0]
        for i, axis in enumerate(self.magnetic_values):
            minv, maxv = self.hardiron_calibration[i]
            axis = min(max(minv, axis), maxv)
            values[i] = (axis - minv) * 200 / (maxv - minv) + -100
        return values
    
    def __get_compass_heading(self):
        return int(math.atan2(self.normalized_values[1], self.normalized_values[0]) * 180.0 / math.pi) + 180
    
    def measure(self):
        try:
            self.magnetic_values = self.sensor.magnetic
            return 1
        except Exception as error:
            return error
        
    def calibrate(self, recalibrate=False):
        if not os.path.exists("tmp.txt"):
            self.calibration_sequence()
            with open("tmp.txt", "w") as f:
                f.write(str(self.hardiron_calibration))
        else:
            with open("tmp.txt", "r") as f:
                self.hardiron_calibration = eval(f.read())
    
    def calibration_sequence(self):
        # calibration for magnetometer X (min, max), Y and Z
        hardiron_calibration = [[1000, -1000], [1000, -1000], [1000, -1000]]

        print("Prepare to calibrate! Twist the magnetometer around in 3D in...")
        print("3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)

        start_time = time.monotonic()

        # Update the high and low extremes
        while time.monotonic() - start_time < 10.0:
            magval = self.sensor.magnetic
            print("Calibrating - X:{0:10.2f}, Y:{1:10.2f}, Z:{2:10.2f} uT".format(*magval))
            for i, axis in enumerate(magval):
                hardiron_calibration[i][0] = min(hardiron_calibration[i][0], axis)
                hardiron_calibration[i][1] = max(hardiron_calibration[i][1], axis) 
        print("Calibration complete:")
        print("hardiron_calibration =", hardiron_calibration)

        self.hardiron_calibration = hardiron_calibration

    normalized_values = property(__get_normalized_values)
    compass_heading = property(__get_compass_heading)


if __name__ == "__main__":
    i2c = board.I2C()
    compass = Compass(i2c)
    
    while True:
        result = compass.measure()
        if result != 1:
            print(result)
            print("Continueing loop...")
            continue

        magvals = compass.magnetic_values
        normvals = compass.normalized_values
        print("magnetometer: %s -> %s" % (magvals, normvals))
        compass_heading = compass.compass_heading
        print("Heading:", compass_heading)
        time.sleep(0.1)