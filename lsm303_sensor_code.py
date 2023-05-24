from time import sleep
import board
import busio
import adafruit_lsm303_accel
import adafruit_lis2mdl
import math
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)
mag = adafruit_lis2mdl.LIS2MDL(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

# Magnetic declination angle for your location (optional)
declination_angle = 0.0

# Calculate 3-axis compass heading
def calculate_compass_heading(mag_data, declination_angle):
    # Normalize magnetometer data
    mag_norm = math.sqrt(mag_data[0]**2 + mag_data[1]**2 + mag_data[2]**2)
    mag_norm_x = math.abs(mag_data[0] / mag_norm)
    mag_norm_y = math.abs(mag_data[1] / mag_norm)
    mag_norm_z = math.abs(mag_data[2] / mag_norm)

    # Calculate heading angle
    heading = math.atan2(mag_norm_y, mag_norm_x)

    # Convert heading angle from radians to degrees
    heading_deg = math.degrees(heading)
    if heading_deg < 0:
        heading_deg += 360.0

    # Adjust for declination angle if necessary
    heading_deg += declination_angle
    if heading_deg < 0:
        heading_deg += 360.0
    elif heading_deg > 360:
        heading_deg -= 360.0

    return heading_deg

# Calculate pitch and roll angles
def calculate_orientation(accel_data):
    accel_x, accel_y, accel_z = accel_data

    pitch = math.atan2(-accel_x, math.sqrt(accel_y**2 + accel_z**2))
    roll = math.atan2(accel_y, accel_z)

    pitch = math.degrees(pitch)
    roll = math.degrees(roll)

    return pitch, roll

# Calculate heading using magnetometer data
def calculate_heading(mag_data):
    mag_x, mag_y, mag_z = mag_data

    heading = math.atan2(mag_y, mag_x)

    heading = math.degrees(heading)
    if heading < 0:
        heading += 360

    return heading

def calculate_spin_down_direction(mag_data):
    mag_x, mag_y, mag_z = mag_data

    spin_down_direction = [mag_x, mag_y, mag_z]
    spin_down_direction /= np.linalg.norm(spin_down_direction)

    return spin_down_direction

while True:
    accel_data = accel.acceleration
    mag_data = mag.magnetic

    pitch, roll = calculate_orientation(accel_data)
    heading = calculate_heading(mag_data)
    spin_down_direction = calculate_spin_down_direction(mag_data)

    # Calculate compass heading
    heading = calculate_compass_heading(mag_data, declination_angle)


    print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f" % accel_data)
    print("Magnetometer (micro-Teslas): X=%0.3f Y=%0.3f Z=%0.3f" % mag_data)
    print("Pitch: %0.3f degrees" % pitch)
    print("Roll: %0.3f degrees" % roll)
    print("Heading: %0.3f degrees" % heading)
    print("Spin-down direction: X=%0.3f Y=%0.3f Z=%0.3f" % tuple(spin_down_direction))
    # Print the compass heading
    print("Compass Heading: {:.2f} degrees".format(heading))
    print("")

    sleep(0.5)
