# 코루틴 함수 만들기 (coroutine function)
# 코루틴 함수 정의 : async def boo():함수 앞에 async 를 붙이면 코루틴 함수가 됨
# 코루틴 호출 : boo() -> 바로실행되지 않고 코루틴 객체를 생성, 이 객체를 코루틴이라고부름, coro = boo()
# 코루틴 실행 : 

import asyncio

async def hello(): 
    print("hello")

coro1 = hello() # coro1이라는 변수로 coroutine함수 객체를 받음
coro2 = hello()

async def main():
    await asyncio.gather(coro1, coro2) # 여러개를 실행할때, 객체를 다시 묶어 새 객체를 만들어야함

main_coro = main()
asyncio.run(main_coro) # main_coro를 호출하여 실행한다 <- 코루틴의 실행
