from fastapi import FastAPI
# 도커안에서 fastapi 설치해서 사용할거임

app = FastAPI()

@app.get("/health-check")
def health_check_handler():
    return {"msg": "ok"}