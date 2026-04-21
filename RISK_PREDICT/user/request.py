from pydantic import BaseModel

# 회원가입 요청에 필요한 데이터 형식
class SignUpRequest(BaseModel):
    email: str
    password: str

# 로그인에 필요한 데이터 형식
class LogInRequest(BaseModel):
    email: str
    password: str


class AuthRequest(BaseModel):
    email: str
    password: str