# 사용할 베이스 이미지 선택
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# pyproject.toml 파일 복사
COPY pyproject.toml ./ poetry.lock ./

# 필요한 Python 라이브러리 설치
RUN pip install poetry
RUN poetry lock --no-update
RUN poetry install

# Django 프로젝트 파일 복사
COPY ../ ./

WORKDIR /usr/src/app/api
# Django 애플리케이션 실행
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
