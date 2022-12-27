
#####
## 
## ws_client.py
## Script to be run on the client machine.
## Connects to rover running ws_server.py which broadcasts data measurements.
## Data received stored in a local sqlite database.
##
#####

import asyncio
import websockets
import sqlite3
import re
import json
import socket

SERVER_IP = "ws://" + socket.gethostbyname('rov.local') + ":5000"
print("Connecting to:", SERVER_IP)

con = sqlite3.connect("rov_local.db")
cur = con.cursor()

#for row in cur.execute('SELECT * from data'):
#    print(row)

def insert_to_db(senddatetime, chamber_tempf, water_tempf, pressure_psi, pressure_ft):
    try:
        cur.execute(f"INSERT INTO data VALUES (NULL, \'{senddatetime}\', {chamber_tempf}, {water_tempf}, {pressure_psi}, {pressure_ft})")
        con.commit()
    except sqlite3.OperationalError:
        print("No such table <data> .... Creating it now")
        create_db()

def create_db():
    cur.execute("""
     CREATE TABLE data (
          dataID integer PRIMARY KEY AUTOINCREMENT
        , senddatetime text
        , chamber_tempF float
        , water_tempF float
        , pressure_psi float
        , pressure_ft floatx);
        """)
    con.commit()

async def get_broadcast():
    async with websockets.connect(SERVER_IP) as websocket:
        message = await websocket.recv()
        return message


if __name__ == "__main__":
    #i=0
    while True:
        #if i == 2:
            #break
        #i += 1
        
        # Get the broadcast message and de-serialize as dictionary
        message = asyncio.run(get_broadcast())
        message = json.loads(message)
        print(message)

        # Insert received data into local database
        insert_to_db(message["senddatetime"], message["chamber_tempF"], message["water_tempF"], message["pressure_psi"], message["pressure_ft"])