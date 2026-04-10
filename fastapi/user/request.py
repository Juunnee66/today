from pydantic import BaseModel, Field


# 사용자가 추가할때, 클라이언트가 서버로 보내는 데이터의 형식
class UserCreateRequest(BaseModel):

    name: str = Field(..., min_length=2, max_length=10)
    job: str

class UserUpdateRequest(BaseModel):
    job: str