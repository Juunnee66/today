
import asyncio
import time


## await 가 사용가능한 곳
# 1) await 는 비동기함수 안에서만 사용가능
# def hello():
#     await asyncio.sleep(3) 
#     #"await" allowed only within async function

# 2) awaitable 한 코드앞에서만 사용가능
async def hi():
    print("start hello..")
    # await time.sleep(2)   # -> 비동기에쓸수없는코드, awaitable 하지않음
    await asyncio.sleep(2)
    print("end hello..")

async def main():
    print("start main..")
    coro = hi()
    await coro # 코루틴 객체 앞에는 await 가능
    # coro가 중첩, hi()가 다끝나야함
    print("end main..")

asyncio.run(main())