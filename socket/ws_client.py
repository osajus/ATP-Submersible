
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

con = sqlite3.connect("rov_local.db")
cur = con.cursor()



#for row in cur.execute('SELECT * from data'):
#    print(row)

def insert_to_db(chamber_tempf, sensor_tempf, pressure_psi, pressure_ft):
    try:
        cur.execute(f"INSERT INTO data VALUES (NULL, {chamber_tempf}, {sensor_tempf}, {pressure_psi}, {pressure_ft})")
        con.commit()
    except sqlite3.OperationalError:
        print("No such table <data> .... Creating it now")
        create_db()
        cur.execute(f"INSERT INTO data VALUES (NULL, {chamber_tempf}, {sensor_tempf}, {pressure_psi}, {pressure_ft})")
        con.commit()

def create_db():
    cur.execute("""
     CREATE TABLE data (
         dataID integer PRIMARY KEY AUTOINCREMENT
        ,chamber_tempF float
        ,sensor_tempF float
        ,pressure_psi float
        ,pressure_ft floatx);
        """)
    con.commit()

async def get_broadcast():
    uri = "ws://192.168.1.142:5000"
    async with websockets.connect(uri) as websocket:
        message = await websocket.recv()
        #print(f"ROV: {message}")
        return message


if __name__ == "__main__":
    #i=0
    while True:
        #if i == 2:
            #break
        #i += 1
        
        # Get the broadcast message
        message = asyncio.run(get_broadcast())
        print(message)
        # Split the message to separate the values from the labels
        split_message = re.split(r'[:,]', message)
        # Insert that message into the local db
        insert_to_db(split_message[1],split_message[3],split_message[5],split_message[7])
