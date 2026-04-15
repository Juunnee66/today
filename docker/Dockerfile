FROM python:3.13-slim 
    # 베이스이미지는 작게, 시간절약
WORKDIR /app
    # 워크디렉토리 지정
COPY main.py .
    # 파일복사
RUN pip install "fastapi[standard]"
    # 여기까지 이미지 만드는데 필요한내용

CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    # 컨테이너안에서 이미지를 "실행" 하는데 필요한 코드