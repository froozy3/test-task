from fastapi import APIRouter, Depends, HTTPException
from services.credit_service import CreditService
from schemas import CreditResponse
from sqlalchemy.orm import Session
from models import get_db

router = APIRouter()


@router.get("/user_credits/{user_id}" )
def get_user_credits(user_id: int, session: Session = Depends(get_db)):
    try:
        return CreditService.get_user_credits(user_id, session)
    except Exception as e:
        print(str(e))