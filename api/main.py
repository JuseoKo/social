from fastapi import FastAPI
from routers import tests  # routers 폴더에 있는 tests.py에서 라우터 가져오기

app = FastAPI()

# tests 라우터 추가
app.include_router(tests.router)