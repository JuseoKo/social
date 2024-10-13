from sqlalchemy import Column, Integer, String
from database.base import Base

class Tests(Base):
    """
    CREATE TABLE tests (
    id INTEGER NOT NULL,
    test VARCHAR,
    PRIMARY KEY (id)
);
    """
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, index=True)
    test = Column(String)

    def __init__(self, id: int, test: str):
        self.id = id
        self.test = test