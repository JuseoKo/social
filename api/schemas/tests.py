# schemas/tests.py
from pydantic import BaseModel

# TestCreate: POST 요청을 위한 입력 스키마
class TestCreateSchema(BaseModel):
    test: str


# Test: 응답을 위한 스키마
class TestSchema(TestCreateSchema):
    id: int

    class Config:
        orm_mode = True