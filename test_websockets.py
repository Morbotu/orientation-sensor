import asyncio
from websockets.server import serve
import time
import board
import adafruit_mma8451
import math

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

        await websocket.send(f"{roll}:{pitch}")

async def main():
    async with serve(echo, "192.168.182.30", 8765):
        print("Available 192.168.182.30:8765...")
        await asyncio.Future()  # run forever

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