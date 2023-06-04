import asyncio
from websockets.server import serve
from websockets.exceptions import ConnectionClosedOK
import socket
import fcntl
import struct
from compass import Compass
from inclinometer import Inclinometer
import board

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

async def send_data(websocket):
    inclinometer.measure()
    compass.measure()
    await websocket.send(f"{inclinometer.angle_yz}:{inclinometer.angle_xz}:{compass.compass_heading}")
    async for message in websocket:
        inclinometer.measure()
        compass.measure()
        try:
            await websocket.send(f"{inclinometer.angle_yz}:{inclinometer.angle_xz}:{compass.compass_heading}")
        except ConnectionClosedOK:
            print("Connection closed")
            

async def main():
    async with serve(send_data, ip, 8765):
        print(f"Available {ip}:8765...")
        await asyncio.Future()  # run forever

i2c = board.I2C()
inclinometer = Inclinometer(i2c)
compass = Compass(i2c)
ip = get_ip_address(b"wlan0")

asyncio.run(main())