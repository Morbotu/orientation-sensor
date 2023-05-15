import asyncio
from websockets.server import serve

async def echo(websocket):
    number = 0
    await websocket.send(str(number))
    async for message in websocket:
        await websocket.send(str(number))
        number += 1

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())