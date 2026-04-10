import time
import asyncio

# 동기식
def a():
    print("A 작업 시작")
    time.sleep(2)
    print("A 작업 종료")

def b():
    print("B 작업 시작")
    time.sleep(2)
    print("B 작업 종료")

start = time.time()
a()
b()
end = time.time()
print(f"실행 소요 시간:{end-start:.2f}")
# 실행 소요 시간:4.01


# 비동기식
# 멈추면 실행권이 넘어감, 먼저끝나는애가 실행권을 다시가져옴
async def a():
    print("A 비동기 작업 시작")
    await asyncio.sleep(5) # 대기발생
    print("A 비동기 작업 종료")

async def b():
    print("B 비동기 작업 시작")
    await asyncio.sleep(2) # 대기발생
    print("B 비동기 작업 종료")

coro1 = a()
coro2 = b()

async def main():
    await asyncio.gather(coro1,coro2)


start = time.time()
asyncio.run(main())
end = time.time()

print(f"비동기 실행 소요 시간:{end-start:.2f}")
# 비동기 실행 소요 시간:2.00