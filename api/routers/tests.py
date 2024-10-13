from fastapi import APIRouter, Depends, HTTPException
from database.base import DBConnection
from sqlalchemy.orm import Session
from schemas.tests import TestSchema, TestCreateSchema
from database.models.test import Tests

router = APIRouter()
db = DBConnection().create_session

# CREATE: 새로운 테스트 데이터 생성
@router.post("/tests/", response_model=TestSchema)
def create_test(test: TestCreateSchema, db: Session = Depends(db)):
    db_test = Tests(id=5, test=test.test)  # id는 자동 생성
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


# READ: 모든 테스트 데이터 조회
@router.get("/tests/", response_model=list[TestSchema])
def read_tests(db: Session = Depends(db)):
    return db.query(Tests).all()

# READ: 특정 테스트 데이터 조회
@router.get("/tests/{test_id}", response_model=TestSchema)
def read_test(test_id: int, db: Session = Depends(db)):
    db_test = db.query(Tests).filter(Tests.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test