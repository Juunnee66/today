from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete

from database.connection import get_session
from database.connection_async import get_async_session
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse


# user 핸들러 함수들을 관리하는 객체
router = APIRouter(tags=["User"])

# 전체 사용자 목록 조회 API
# GET /users
@router.get(
        "/users", 
        summary="전체 사용자 목록 조회 API",
        status_code=status.HTTP_200_OK,
        response_model=list[UserResponse],
)
async def get_users_handler( # 비동기
    # Depends: FastAPI에서 의존성(get_session)을 자동으로 실행,주입,정리
    session = Depends(get_async_session), # 비동기
):
    # statment : 구문(명령문)
    stmt = select(User) # SELECT * FROM user;
    result = await session.execute(stmt) # i/o 대기 발생
    users = result.scalars().all() # [user1, user2, user3, ...]
    return users

# 사용자 정보 검색 API
# GET /users/search?name=alex
# GET /users/search?job=student
@router.get(
        "/users/search",
        summary="사용자 정보 검색 API",
        response_model=list[UserResponse],
)
async def search_user_handler(
    name: str | None = Query(None),
    job: str | None = Query(None),
    session = Depends(get_async_session)
):
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다."
        )
    
    stmt = select(User) # 쿼리작성부분
    if name: # 조건에따른 쿼리 확장부분
        stmt = stmt.where(User.name == name)
    if job:
        stmt = stmt.where(User.job == job)

    result = await session.execute(stmt) # 쿼리실행 -> I/O 발생
    users = result.scalars().all() 
    return users


# 단일 사용자 데이터 조회 API
# GET /users/{user_id} -> {user_id}번 사용자 데이터 조회
@router.get(
        "/users/{user_id}",
        summary="단일 사용자 데이터 조회 API",
        response_model=UserResponse,
)
async def get_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_async_session)
):
    # ex) SELECT * FROM user WHERE id = 42;
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar() # 존재하면 user객체, 존재하지 않으면 None

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
    )
    return user

# 회원 추가 API
# POST /users
@router.post(
    "/users",
    summary="회원 추가 API", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user_handler(
    body: UserCreateRequest,
    session = Depends(get_async_session)
):
    
    # 사용자 데이터를 넘겨 받는다 + 데이터 유효성 검사
    # context manager 를 벗어나는 순간 자동으로 close() 호출
    new_user = User(name=body.name, job=body.jb) # 객체생성
    session.add(new_user) # 객체를 세션에 추가 -> 데이터변경내용을 관리해라, 
    await session.commit() # 변경사항 저장을 DB에 요청
    await session.refresh(new_user) # DB에서 자동생성된 id, created_at 불러옴
    return new_user


# 회원 정보 수정 API
# PUT : 전체교체
# PATCH : 일부 교체
# PATCH /users/{user_id}
@router.patch(
    "/users/{user_id}",
    summary="회원 정보 수정 API",
    response_model=UserResponse, # user가 반환될때 형식확인해줌
)
async def update_user_handler(
    # 1) 클라이언트로부터 수정할 데이터를 받는다
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_async_session)
):
    # 2) 처리
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    user.job = body.job
    await session.commit() #user 상태(job변경)를 DB에 반영
    return user 

# 회원 삭제 API
# DELETE /users/{user_id}
@router.delete(
    "/users/{user_id}",
    summary="회원 삭제 API",
    status_code=status.HTTP_204_NO_CONTENT, # 응답본문이 비었을때
)
async def delete_user_handler(
    user_id: int,
    session = Depends(get_async_session)
):
    # # 1) get+delete : 정보 불러와서(조회) 지우기
    # stmt = select(User).where(User.id == user_id)
    # result = await session.execute(stmt)
    # user = result.scalar()

    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, # 존재하지않는 사용자를 삭제시도하면 404
    #         detail="User Not Found",
    # )

    # await session.delete(user) # 객체를 삭제
    # # session.expunge(user) => 세션의 추적 대상에서 제거
    # await session.commit()

    # 2) 바로삭제, 없는 정보로 지우려고하면 무시함
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt) # 삭제
    await session.commit() # 확정

    # await 가 붙는 대표적 위치들 
    # session.execute()
    # session.commit()
    # session.refresh()