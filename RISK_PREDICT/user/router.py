from fastapi import APIRouter, status, Depends, HTTPException, Body
from fastapi.security import HTTPBearer
from sqlalchemy import select  

from auth.jwt import create_access_token, verify_user
from auth.password import hash_password, verify_password
from database.connection import get_session
from user.models import User, HealthProfile
from user.request import SignUpRequest, LogInRequest, HealthProfileRequest
from user.response import UserResponse


router = APIRouter(tags=["User"])

 # 회원가입 API
@router.post(
    "/users",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def signup_handler(
    body: SignUpRequest,
    session = Depends(get_session),
):
    # 1) 이메일 중복 검사 -> DB 에 저장된 데이터중 중복된 이메일이 있는지 확인
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 이메일입니다,"
        )
    
    # 2) 비밀번호 해싱->암호화
    password_hash = hash_password(plain_password=body.password)

    # 3) 회원 데이터 저장
    new_user = User(
        email=body.email,
        password_hash=password_hash,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user) #id, created_at 새로고침

    return new_user

# 로그인 API
@router.post(
    "/users/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)
async def login_handler(
    body: LogInRequest,
    session = Depends(get_session),

):
    # 1) email로 사용자 조회
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록되지 않은 이메일입니다.",
        )

    # 2) body.password <> 사용자.password_hash 검증
    verified = verify_password(
        plain_password=body.password,
        password_hash=user.password_hash
    )
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 일치하지 않습니다.",
        )

    # 3) JWT(JSON Web Token) 발급
    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token}


# 건강 프로필 생성
@router.post(
    "/health-profiles",
    summary="건강 프로필 생성 API",
    status_code=status.HTTP_201_CREATED,
)
async def create_health_profile_handler(
    # 클라이언트가 보낸 Authorization Header를 읽어줌
    user_id = Depends(verify_user),
    body: HealthProfileRequest = Body(...),
    session = Depends(get_session),
):
    # 1) 건강프로필 중복검사
    stmt = (
        select(HealthProfile)
        .where(HealthProfile.user_id == user_id)
    )

    result = await session.execute(stmt)
    existing_profile = result.scalar()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 건강 프로필이 존재합니다.",
        )
    # 2) 건강 프로필 생성 & 저장
    profile_data = body.model_dump() # 덤프가 자동으로 딕셔너리 만들어줌
    new_profile = HealthProfile(
        user_id=user_id, **profile_data)


    session.add(new_profile)
    await session.commit()
    await session.refresh(new_profile)

    return new_profile

