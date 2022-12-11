import os
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import FileResponse
from fastapi.params import Body
from pydantic import BaseModel, Field


# Configure FastAPI
app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"status:": "API okay"}

@app.get("/rov")
def get_status():
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
            detail="API okay")
@app.get("/test")
def get_status():
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
            detail="test okay")

@app.post("/pull")
def git_pull():
    f = open('/home/pi/rov/GITPULLMASTER', 'w')
    f.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, 
            detail="done")
