from fastapi import FastAPI, status
from user.router import router

app = FastAPI()
app.include_router(router)

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


