# SQLAlchemy 를 이용해 DB와 연결하는 코드

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# 데이터베이스 접속
DATABASE_URL = "sqlite+aiosqlite:///./local.db"

# Engine : DB와 접속을 관리하는 객체
async_engine = create_async_engine(DATABASE_URL, echo=True) # echo: 중간에 발생하는 sql을 다 출력해줌


# Session: 한번의 DB 요청-응답
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    # 데이터를 어떻게 다룰지에대한 옵션
    autocommit = False,
    autoflush=False,
    expire_on_commit=False,
)

#SQLAlchemy 세션을 관리하는 함수
async def get_async_session():
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()
