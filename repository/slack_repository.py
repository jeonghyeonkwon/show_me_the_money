from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db

from models.slack import SlackLog


class SlackRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def insert_log(self, slack_log: SlackLog) -> None:
        self.session.add(instance=slack_log)
        self.session.commit()
        return
