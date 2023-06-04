import time
import math
import board
import adafruit_lis2mdl

class Compas:
    def __init__(self, i2c) -> None:
        self.sensor = adafruit_lis2mdl.LIS2MDL(i2c)
        self.hardiron_calibration = [[-37.05, 122.69999999999999], [-71.1, 49.05], [-117.3, 27.15]]

    def normalize(self, _magvals):
        ret = [0, 0, 0]
        for i, axis in enumerate(_magvals):
            minv, maxv = self.hardiron_calibration[i]
            axis = min(max(minv, axis), maxv)  # keep within min/max calibration
            ret[i] = (axis - minv) * 200 / (maxv - minv) + -100
        return ret
    
    def measure(self):
        return self.sensor.magnetic

if __name__ == "__main__":
    i2c = board.I2C()
    compas = Compas(i2c)
    
    while True:
        magvals = compas.measure()
        normvals = compas.normalize(magvals)
        print("magnetometer: %s -> %s" % (magvals, normvals))
        compass_heading = int(math.atan2(normvals[1], normvals[0]) * 180.0 / math.pi)
        compass_heading += 180
        print("Heading:", compass_heading)
        time.sleep(0.1)