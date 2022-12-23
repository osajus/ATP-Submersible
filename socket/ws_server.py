
import asyncio
import datetime
import random
import websockets
from sensors import BMP180
from sensors import SSC





tcouple = BMP180.BMP()
press = SSC.SSC30()
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
        message = str(
            f"\nChamber Temp 'F: {tcouple.get_tempF()}"
            f"\nSensor Temp 'F: {press.get_tempF()}"
            f"\nPressure PSI: {press.get_pressPSI()}"
            f"\nPressure FT: {press.get_pressFT()}"
        )
        
        websockets.broadcast(CONNECTIONS, message)
        await asyncio.sleep(3)


async def main():
    async with websockets.serve(register, "192.168.1.142", 5000):
        await show_temp()


if __name__ == "__main__":
    asyncio.run(main())