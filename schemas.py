from typing import Optional, List
from pydantic import BaseModel
from datetime import date





class ClosedCredit(BaseModel):
    credit_issued_date: date  # Дата выдачи кредита
    is_closed: bool = True  # Булевое значение: кредит закрыт
    return_date: date  # Дата возврата кредита
    body: float  # Сумма выдачи
    percent: float  # Нараховані відсотки
    total_payments: float  # Сума платежів за кредитом




class OpenCredit(BaseModel):
    credit_issued_date: date  
    is_closed: bool = False  
    return_date: date  
    body: float  
    percent: float 
    principal_payments: float  
    interest_payments: float  


class CreditResponse(BaseModel):
    closed_credits: List[ClosedCredit] = []
    open_credits: List[OpenCredit] = [] 



