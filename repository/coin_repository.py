from fastapi import Depends
from db.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.coin import Coin


class CoinRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, coin_list: list[Coin]):
        prev_market = list(self.session.scalars(select(Coin.market)))

        new_market: list[str] = list(map(lambda obj: obj.market, coin_list))

        difference = [x for x in new_market if x not in prev_market]

        new_coin = [obj for obj in coin_list if obj.market in difference]

        self.session.add_all(instances=new_coin)
        self.session.commit()

        return new_coin
