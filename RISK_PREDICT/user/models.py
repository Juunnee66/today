from datetime import datetime

from database.orm import Base


from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Float, Boolean
from sqlalchemy.orm import MappedColumn, mapped_column


class User(Base):
    __tablename__ = "user"

    id: MappedColumn[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    email: MappedColumn[str] = mapped_column(String(256), unique=True,)
    password_hash: MappedColumn[str] = mapped_column(String(256))
    created_at: MappedColumn[datetime] = mapped_column(
        DateTime, server_default=func.now() # db에게 현재시간을 찍는 함수를 찾아서 써라고 시키는것
    )

class HealthProfile(Base):
    __tablename__ = "health_profile"

    id: MappedColumn[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: MappedColumn[int] = mapped_column(
        ForeignKey("user.id"), unique=True
    )
    age: MappedColumn[int] = mapped_column(Integer)
    height_cm: MappedColumn[float] = mapped_column(Float)
    weight_kg: MappedColumn[float] = mapped_column(Float)
    smoking: MappedColumn[bool] = mapped_column(Boolean)
    exercise_per_week: MappedColumn[int] = mapped_column(Integer)