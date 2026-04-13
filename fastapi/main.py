import anyio
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from user.router import router


#스레드풀 크기조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)



def aws_sync():
    #AWS 서버랑 통신(예:2초)
    return

from starlette.concurrency import run_in_threadpool

@app.get("/async")
async def async_handler():
    await run_in_threadpool(aws_sync) # 동기 함수를 비동기 방식으로 실행하게 해주는 유틸리티 함수
    return {"msg": "ok"}


# # 테스트
# # python decorator : 함수를 꾸며주는, 함수에 추가기능을 부여하는 문법
# # get 요청이 들어오면 root handler 함수 실행
# @app.get("/", status_code=200) # 성공인거 확인하려고 상태코드 넣음
# def root_handler():
#     return {"ping": "pong"}

# # GET /hello : hello 경로에서 get 요청을 보내면 함수가 실행됨
# @app.get("/hello", status_code=status.HTTP_200_OK) 
# def hello_handler():
#     return {"msg" : "Hello from FastAPI!"}


