from fastapi import FastAPI
# 도커안에서 fastapi 설치해서 사용할거임
from sqlalchemy import text
from connection import SessionFactory

app = FastAPI()

@app.get("/health-check")
def health_check_handler():
    # orm 셋팅은 안함
    with SessionFactory() as session:
        stmt = text("SELECT * FROM user LIMIT 1;")
        row = session.execute(stmt).fetchone()
    return {"user": row._asdict()}

