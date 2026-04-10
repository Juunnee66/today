# SQLAlchemy 를 이용해 DB와 연결하는 코드

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속
DATABASE_URL = "sqlite:///./local.db"

# Engine : DB와 접속을 관리하는 객체
engine = create_engine(DATABASE_URL, echo=True) # echo: 중간에 발생하는 sql을 다 출력해줌


# Session: 한번의 DB 요청-응답
SessionFactory = sessionmaker(
    bind=engine,
    # 데이터를 어떻게 다룰지에대한 옵션
    autocommit = False,
    autoflush=False,
    expire_on_commit=False,
)

#SQLAlchemy 세션을 관리하는 함수
def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
