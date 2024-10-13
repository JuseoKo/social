# 사용할 베이스 이미지 선택
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 애플리케이션 파일 복사 COPY 호스트주소 컨테이너주소
COPY . .

# 필요한 Python 라이브러리 설치
RUN pip install -r requirements.txt

# uvicorn을 사용하여 FastAPI 애플리케이션 실행
WORKDIR /usr/src/app/api
# uvicorn을 사용하여 FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]