import asyncio
import aiohttp
import time

async def test1(session,url):
    async with session.get(url) as response:
        status = response.status
        return status



async def test1():
    async with aiohttp.ClientSession() as session:
        responses = []
        async with asyncio.TaskGroup() as tg:
            pass






test_1_time_start = time.perf_counter()
asyncio.run(test1())
test_1_time_end = time.perf_counter()
print(f"Total time for test 1 is {test_1_time_end - test_1_time_start}")
