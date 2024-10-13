import pandas as pd
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import orm
from utils.patterns import SingletonMeta
from loguru import logger
from sqlalchemy.dialects.postgresql import insert

Base = orm.declarative_base()


class DBConnection(metaclass=SingletonMeta):
    """
    DB세션을 연결해주는 클래스입니다.
    """

    def __init__(self):
        # env load
        env_path = os.path.dirname(os.path.dirname(os.getcwd()))
        load_dotenv(f"{env_path}/.env")
        load_dotenv(".env")
        print(env_path)
        self.engines = create_engine(
            f'postgresql+psycopg2://{os.getenv("API_USER")}:{os.getenv("API_PASSWORD")}@{os.getenv("API_HOST")}:5432/{os.getenv("API_NAME")}'
            )
        logger.info(f"Connection created")
        logger.info(f"URL: {self.engines.url}")

    def create_session(self):
        """
        sqlalchemy session 반환
        :return:
        """
        return sessionmaker(bind=self.engines)()

    def get_url(self):
        """
        url 반환
        :param db: api-db or airflow-db
        :return:
        """
        return self.engines.url


    def get_db(self):
        """
        FastAPI 의존성 주입을 위한 DB 세션을 생성하고 반환하는 함수
        """
        db = self.create_session()
        try:
            yield db
        finally:
            db.close()



    def __del__(self):
        self.engines.dispose()

class DBCrud(DBConnection, metaclass=SingletonMeta):
    """
    DB crud를 수행하는 클래스입니다.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def pg_bulk_upsert(
        session, df: pd.DataFrame, model, uniq_key: list, batch_size: int = 100
    ) -> int:
        """
        데이터프레임을 bulk_upsert 하는 함수입니다.
        :param session:
        :param df:
        :param model: sql알케미 모델
        :param uniq_key:
        :return:
        """
        model_columns = [c.name for c in model.__table__.columns]
        df_columns = df.columns.tolist()
        cnt = 0

        for start in range(0, len(df), batch_size):
            # 데이터프레임을 딕셔너리로 변환
            data = df.iloc[start : start + batch_size].to_dict(orient="records")

            # upsert 문을 생성
            stmt = insert(model).values(data)

            # update 할 컬럼 설정
            update_dict = {
                col: insert(model).excluded[col]
                for col in df_columns
                if col in model_columns and col not in uniq_key
            }

            update_stmt = stmt.on_conflict_do_update(
                index_elements=uniq_key, set_=update_dict
            )
            session.execute(update_stmt)
            cnt += len(data)
        session.commit()
        return cnt