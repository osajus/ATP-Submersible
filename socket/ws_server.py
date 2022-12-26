
import asyncio
from datetime import datetime
import websockets
import json
from sensors import BMP180
from sensors import SSC
import socket

# Amount of time between each broadcast.
BROADCAST_FREQ = 0.5

MY_IP = socket.gethostbyname(socket.gethostname() + ".local")
print("Running on:", MY_IP)

# Instantiate chamber pressure sensor 
tcouple = BMP180.BMP()
# Instantiate wet media sensor
press = SSC.SSC30()
# Set websocket 
CONNECTIONS = set()

async def register(websocket):
    # Keep track of all connections
    CONNECTIONS.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        CONNECTIONS.remove(websocket)


async def send_message():
    # Broadcast a message to all connections
    while True:
        # Wait a set number of seconds before new broadcast as we
        #   must yield control to the event loop between each message
        await asyncio.sleep(BROADCAST_FREQ)
        # Get current date/time and format it
        dt = datetime.now()
        sendtime = dt.strftime('%Y-%m-%d %X:%f')
        # Create message dictionary
        message = {
              "senddatetime": sendtime
            , "chamber_tempF": tcouple.get_tempF()
            , "sensor_tempF": press.get_tempF()
            , "pressure_psi": press.get_pressPSI()
            , "pressure_ft": press.get_pressFT()
        }
        # Serialize dictionary so it can be broacast
        message = json.dumps(message)
        # Sent the message (Consider switching to concurrent in future)
        websockets.broadcast(CONNECTIONS, message)
        


async def main():
    async with websockets.serve(register, MY_IP, 5000):
        await send_message()


if __name__ == "__main__":
    asyncio.run(main())