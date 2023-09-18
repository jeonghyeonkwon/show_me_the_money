from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db

from models.candle import MonthCandle


class CandleRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def insertMonth(self, month_list: list[MonthCandle]):
        where_list = [(obj.market, obj.target_date) for obj in month_list]
        where_in_str = ""

        for index, obj in enumerate(where_list):
            if index == len(where_list) - 1:
                where_in_str += f" ( '{obj[0]}', '{obj[1]}') "
            else:
                where_in_str += f" ( '{obj[0]}', '{obj[1]}'), "

        result = self.session.execute(
            f"SELECT market, date_format(target_date,'%Y-%m-%dT%T')  FROM month_candle WHERE (market, target_date) IN ({where_in_str})"
        )

        copy_list = month_list[:]

        # 이미 있는 리스트
        for duplication_list in result:
            copy_list = [
                obj
                for obj in copy_list
                if not (
                    (duplication_list[0] == obj.market)
                    & (duplication_list[1] == obj.target_date)
                )
            ]

        self.session.add_all(instances=copy_list)

        self.session.commit()
        return

    def select_month(self):
        l = self.session.scalars(
            select(MonthCandle).order_by(MonthCandle.target_date.asc()).limit(40)
        ).all()

        return l
