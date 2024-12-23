from schemas import CreditResponse, ClosedCredit, OpenCredit
from typing import List
from sqlalchemy.orm import Session
from datetime import date
from models import Credit, get_db
from fastapi import Depends, HTTPException


class CreditService:
    @staticmethod
    def get_user_credits(user_id: int, session: Session = Depends(get_db)) -> CreditResponse:
        try:
            credits = session.query(Credit).filter(
                Credit.user_id == user_id).all()
            print(f"Credits:{credits}")
            closed_credits = []
            open_credits = []
            for credit in credits:
                if credit.actual_return_date:
                    closed_credits.append(ClosedCredit(credit_issued_date=credit.issuance_date,
                                                       return_date=credit.return_date, body=credit.body, percent=credit.percent, total_payments=CreditService.calculate_percent(credit.body, credit.percent)))
                else:
                    open_credits.append(OpenCredit(credit_issued_date=credit.issuance_date, return_date=credit.return_date, overdue_days=CreditService.calculate_days(credit.return_date),

                                                   body=credit.body, percent=credit.percent, principal_payments=0.0, interest_payments=float(credit.body * credit.percent / 100)))
            print(closed_credits, open_credits)
            return CreditResponse(closed_credits=closed_credits, open_credits=open_credits)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

    @staticmethod
    def calculate_percent(body: float, percent: float) -> float:
        return float(body + (body * percent / 100))

    @staticmethod
    def calculate_days(return_date: date) -> int:
        delta = date.today() - return_date
        return delta.days
