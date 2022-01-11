from datetime import datetime
from enum import Enum

import random
def random_date_with_days(start_date, days_between_dates):
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

def random_date_from_dates(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    return random_date_with_days(start_date, days_between_dates)

class LoanStatus(Enum):
    PENDING = 1
    PAYOFF = 2

class LoanDataFactory:
    @staticmethod
    def create(od, s, c):
        return {
            "orig_dt": od,
            "status": s, 
            "close_date": c,
        }


loan_data = [
    LoanDataFactory.create(datetime(2021, 1, 1), LoanStatus.PENDING, None),
    LoanDataFactory.create(datetime(2021, 2, 1), LoanStatus.PAYOFF, datetime(2021, 5, 1)),
    LoanDataFactory.create(datetime(2021, 6, 1), LoanStatus.PAYOFF, datetime(2021, 9, 1)),
]

class TUDataFacotry:
    @staticmethod
    def create(agg502, agg503, fico_score, atap01, reported_income):
        return  {
        "agg502": agg502,
        "agg503": agg503,
        "fico_score": fico_score,
        "atap01": atap01,
        "reported_income": reported_income,
    }

tu_data = [
   
]

class ProsperApplicationDataFactory:
    @staticmethod
    def create(requested_amount, app_date, stated_income):
        return {
            "requested_amount":requested_amount,
            "app_date": app_date,
            "stated_income": stated_income,
        }

application_data = [
    ProsperApplicationDataFactory.create(3000, datetime(2021, 12, 1), 80000)
]


from typing import Optional

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}