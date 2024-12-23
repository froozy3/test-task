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
    credit_issued_date: date  # Дата выдачи кредита
    is_closed: bool = False  # Булевое значение: кредит открыт
    return_date: date  # Крайняя дата возврата кредита
    overdue_days: int  # Количество дней просрочки кредита
    body: float  # Сумма выдачи
    percent: float  # Нараховані відсотки
    principal_payments: float  # Сума платежів по тілу
    interest_payments: float  # Сума платежів по відсоткам


class CreditResponse(BaseModel):
    # Список закрытых кредитов
    closed_credits: List[ClosedCredit] = []
    open_credits: List[OpenCredit] = [] # Список открытых кредитов



