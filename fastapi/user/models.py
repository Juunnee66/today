from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database.orm import Base


class User(Base):
    __tablename__="user"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    ) # 기본키지정
    name: Mapped[str] = mapped_column(String(32))
    job: Mapped[str] = mapped_column(String(32))
    created_at : Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now() #레코드 생성시각 자동저장
    )