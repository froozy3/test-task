
from sqlalchemy.orm import Session
from fastapi import UploadFile, Depends, HTTPException
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from datetime import date, datetime
from typing import List
from schemas import *
import pandas as pd
from models import *
from routers.credit import router as credit_router
from routers.plan import router as plan_router

app = FastAPI()


app.include_router(credit_router, tags=["get_credits"])
app.include_router(plan_router, tags=["upload_plan"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
