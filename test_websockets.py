import asyncio
from websockets.server import serve
from websockets.exceptions import ConnectionClosedOK
import time
import board
import adafruit_mma8451
import math
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

async def echo(websocket):
    x, y, z = sensor.acceleration
    await websocket.send("0:0")
    async for message in websocket:
        x, y, z = sensor.acceleration
        try:
            pitch = math.degrees(math.atan(y / z))
        except ZeroDivisionError:
            pitch = 90 if y > 0 else -90

        try:
            roll = math.degrees(math.atan(x / z))
        except ZeroDivisionError:
            roll = 90 if x > 0 else -90

        try:
            await websocket.send(f"{roll}:{pitch}")
        except ConnectionClosedOK:
            print("Connection closed")
            

async def main():
    async with serve(echo, ip, 8765):
        print(f"Available {ip}:8765...")
        await asyncio.Future()  # run forever

ip = get_ip_address(b"wlan0")
i2c = board.I2C()
while True:
    try:
        print("Waiting for I2C...")
        time.sleep(5)
        # Initialize MMA8451 module.
        sensor = adafruit_mma8451.MMA8451(i2c)
        print("Done")
        break
    except OSError:
        print("Connection failed...")
        print("Trying again...")

asyncio.run(main())