from fastapi import APIRouter, Depends, HTTPException, UploadFile
from services.plan_service import PlanService
from sqlalchemy.orm import Session
from models import get_db

router = APIRouter()


@router.post("/plans_insert")
async def upload_plan(file: UploadFile, session: Session = Depends(get_db)):
    content = await file.read()
    return PlanService.upload_plan(file=content, session=session)


@router.get("/plans_performance")
def get_perfomance_plan(date_str:str, session: Session = Depends(get_db)):
    return PlanService.get_plan_performance(date_str=date_str, session=session)
