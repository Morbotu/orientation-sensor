import time
import board
import busio
import adafruit_lis2mdl

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create LSM303AGR instance
sensor = adafruit_lis2mdl.LIS2MDL(i2c)


# Calibration variables
min_x = min_y = min_z = float('inf')
max_x = max_y = max_z = float('-inf')

# Number of calibration samples
num_samples = 100

print("Starting magnetometer calibration...")
print("Move the LSM303AGR module around in all directions until prompted to stop.")

# Collect calibration samples
for _ in range(num_samples):
    mag_x, mag_y, mag_z = sensor.magnetic
    min_x = min(min_x, mag_x)
    min_y = min(min_y, mag_y)
    min_z = min(min_z, mag_z)
    max_x = max(max_x, mag_x)
    max_y = max(max_y, mag_y)
    max_z = max(max_z, mag_z)
    if num_samples < 10 and (max_x == mag_x or max_y == mag_y or max_z == mag_z or min_x == mag_x or min_y == mag_y or min_z == mag_z):
        num_samples += 10
        print("Calculating more...")
    time.sleep(0.1)  # Delay between samples

print("Calibration completed.")
print("Minimum values (x, y, z):", min_x, min_y, min_z)
print("Maximum values (x, y, z):", max_x, max_y, max_z)

# Calculate calibration offsets
offset_x = (max_x + min_x) / 2
offset_y = (max_y + min_y) / 2
offset_z = (max_z + min_z) / 2

# Calculate calibration scales
scale_x = (max_x - min_x) / 2
scale_y = (max_y - min_y) / 2
scale_z = (max_z - min_z) / 2

print("Calibration offsets (x, y, z):", offset_x, offset_y, offset_z)
print("Calibration scales (x, y, z):", scale_x, scale_y, scale_z)

# Apply calibration values to the magnetometer
sensor.magnetic_offsets = (offset_x, offset_y, offset_z)
sensor.magnetic_scales = (scale_x, scale_y, scale_z)