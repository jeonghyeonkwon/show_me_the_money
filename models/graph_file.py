from sqlalchemy import Column, Integer, String, DateTime, BigInteger

from db.database import Base
from util.util import UtilService
from models.enum import GraphType


class GraphFile(Base):
    __tablename__ = "graph_file"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20))
    file_path = Column(String(100))
    created_at = Column(DateTime, default=UtilService.get_time())

    @classmethod
    def create(cls, type: GraphType, path: str):
        return cls(type=type.value, file_path=path)
