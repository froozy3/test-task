from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import pandas as pd
from models import get_db, Plan, Credit, Payment
from io import BytesIO
from datetime import datetime


class PlanService:
    @staticmethod
    def upload_plan(file: bytes, session: Session = Depends(get_db)):
        try:
            file_io = BytesIO(file)
            df = pd.read_excel(file_io)
            data_dict = df.to_dict(orient='records')
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error reading file: {str(e)}")

        new_plans = []

        for data in data_dict:
            month = data['Місяць']
            category_id = data['Категорія']
            suma = data['Сума']

            print(month, category_id, suma)
            existing_plan = session.query(Plan).filter(
                Plan.period == month, Plan.category_id == category_id).first()

            if existing_plan:
                raise HTTPException(
                    status_code=400, detail="Plan already exist")

            day = month[-2:]
            if not day.endswith('01'):
                raise HTTPException(
                    status_code=400, detail=f"Day must be started with 01. You: {day}")

            if pd.isnull(suma):
                raise HTTPException(status_code=400, detail="Suma stored null")

            period = datetime.strptime(month, '%Y-%m-%d').date()
            new_plans.append(
                Plan(period=period, sum=suma, category_id=category_id))

            session.add_all(new_plans)
            session.commit()

            return {"message": "Plan has been successfully added to the database."}

    @staticmethod
    def get_plan_performance(date_str: str, session):
        plans = session.query(Plan).all()

        result = []

        date_check = datetime.strptime(date_str, "%Y-%m-%d").date()

        for plan in plans:
            month = datetime.strftime(plan.period, "%Y-%m")

            if date_check < plan.period:
                continue  

            
            if plan.category_id == 3:
                
                issued_credits_sum = PlanService.calculate_issued_credits(plan.period, date_check, session)

                
                performance_percentage = PlanService.calculate_perfomance_precentage(
                    issued_credits_sum, plan.sum
                )

                
                result.append({
                    "month": month,
                    "category": plan.category_id,
                    "planned_amount": plan.sum,
                    "fact_issued_credits": issued_credits_sum,
                    "performance_percentage": performance_percentage
                })

        return result

    @staticmethod
    def calculate_issued_credits(plan_period, date_check, session: Session) -> float:
        if date_check < plan_period:
            raise ValueError(
                "The verification date must be later than or equal to the start date of the plan month."
            )

        issued_credits = session.query(Credit).filter(
            Credit.issuance_date >= plan_period,
            Credit.issuance_date <= date_check    
        ).with_entities(
            Credit.body  
        ).all()

       
        total_issued = sum([credit.body for credit in issued_credits])

        return total_issued

    @staticmethod
    def calculate_perfomance_precentage(fact_amount: float, planned_sum: float) -> float:
        if planned_sum == 0:
            return 0.0  
        performance_percentage = (fact_amount / planned_sum) * 100
        return round(performance_percentage, 2)  
