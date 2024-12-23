
from sqlalchemy.orm import Session
from fastapi import UploadFile, Depends, HTTPException
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from datetime import date, datetime
from typing import List
from schemas import *
import pandas as pd
from models import *
from routers.user_credits import router as credit_router

app = FastAPI()


# @app.post("")
# def upload_plans(file: str, session: Session = Depends(get_db)):
#     df = pd.read_excel(file)
#     data_dict = df.to_dict(orient='records')
#     for data in data_dict:
#         month = data['Місяць']
#         category_id = data['Категорія']
#         suma = data['Сума']

#         print(month, category_id, suma)
#         existing_plan = session.query(Plan).filter(
#             Plan.period == month, Plan.category_id == category_id).first()

#         if existing_plan:
#             raise HTTPException(status_code=400, detail="Plan already exist")

#         day = month[-2:]
#         if not day.endswith('01'):
#             raise HTTPException(
#                 status_code=400, detail=f"Day must be started with 01. You: {day}")

#         if pd.isnull(suma):
#             raise HTTPException(status_code=400, detail="Suma stored null")


app.include_router(credit_router, tags=["get_credits"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
    session = next(get_db())
    path = r"C:\Users\Владик\Desktop\excel.xlsx"
    # upload_plans(file=path, session=session)
