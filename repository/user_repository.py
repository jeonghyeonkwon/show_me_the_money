from fastapi import Depends
from db.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.user import User, UserAccessLog


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    # 있는지 검증
    def is_exists_user(self, userId: str) -> str:
        return self.session.scalar(select(User.userId).where(User.userId == userId))

    # 초기 유저 생성
    def create(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user

    def findByUserId(self, userId: str) -> User:
        return self.session.scalar(select(User).where(User.userId == userId))

    def insertLog(self, obj: UserAccessLog) -> None:
        self.session.add(instance=obj)
        self.session.commit()
