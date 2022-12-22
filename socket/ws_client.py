
import asyncio
import websockets


async def get_broadcast():
    uri = "ws://192.168.1.142:5000"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        print(f"ROV: {message}")


if __name__ == "__main__":
    while True:
        asyncio.run(get_broadcast())