import os
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import FileResponse
from fastapi.params import Body
from pydantic import BaseModel, Field

# Configure FastAPI
app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"status:": "You shouldn't be seeing this."}

@app.get("/rov")
def get_status():
    tempf = os.system("/usr/bin/vcgencmd measure_temp | awk -F \"[=']\" '{print($2 * 1.8)+32}'")
    tempf = (tempf * .001 * 1.8) + 32
    uptime_min =  os.system("uptime ")
    uptime_min = round((uptime_min / 60), 1)
    testdict = {"Uptime minutes": uptime_min, "Temp 'f": tempf, "API Status": "Okay"}
    return testdict

@app.post("/rov/pull")
def git_pull():
    f = open('/home/pi/rov/GITPULLMASTER', 'w')
    f.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
            detail="done")
