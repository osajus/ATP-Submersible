
import asyncio
import datetime
import random
import websockets
from thermocouple import BMP180





tcouple = BMP180.BMP()
CONNECTIONS = set()

async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def show_time():
    while True:
        message = datetime.datetime.utcnow().isoformat() + "Z"
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(random.random() * 2 + 1)

async def show_temp():
    while True:
        message = str(tcouple.get_tempF())
        
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(random.random() * 2 + 1)


async def main():
    async with websockets.serve(register, "192.168.1.142", 5000):
        await show_temp()


if __name__ == "__main__":
    asyncio.run(main())