from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.database import get_db
from models.graph_file import GraphFile


class GraphRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def insert_graph(self, graph_file: GraphFile):
        self.session.add(instance=graph_file)
        self.session.commit()
        return
