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
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
            detail="API okay")

@app.post("/rov/pull")
def git_pull(payload: dict = Body(...)):
    f = open('/home/pi/rov/GITPULLMASTER', 'w')
    f.close()
    f = open('/home/pi/rov/footxt', 'w')
    f.write(payload)
    f.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
            detail="done")
