import asyncio
import time

#비동기식을 잘쓴경우
async def good_job():
    print("[G]양보합니다...")
    await asyncio.sleep(2)
    print("[G]돌려받았습니다.")

async def bad_job():
    print("[B]양보 안합니다...")
    await asyncio.sleep(5)
    print("[B]계속 진행")

async def main1():
    coro1 = good_job()
    coro2 = bad_job()
    await asyncio.gather(coro1,coro2)

start = time.time()
asyncio.run(main1())
end = time.time()
print(f"{end-start:.2f}")



# 비동기 함수안에 동기함수가 섞여있어 blocking이발생
async def request1():
    print("[1]새로운 웹 요청...")
    await asyncio.sleep(2)
    print("[1]응답...")

async def request2():
    print("[2]새로운 웹 요청...")
    time.sleep(5)      # blocking
    print("[2]응답...")

async def main2():
    coro1 = request1()
    coro2 = request2()
    await asyncio.gather(coro1,coro2)

start = time.time()
asyncio.run(main2())
end = time.time()
print(f"{end-start:.2f}")