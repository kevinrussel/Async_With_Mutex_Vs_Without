import asyncio
import aiohttp
import time

async def test1_url(session,url):
    async with session.get(url) as response:
        status = response.status
        return status



async def test1():
    async with aiohttp.ClientSession() as session:
        responses = []
        with open('data.txt', 'r') as file:
            lines = file.readlines()
        async with asyncio.TaskGroup() as tg:
            for line in lines:
                task = tg.create_task(test1_url(session,line))
                responses.append(task)

    for value in responses:
        print(value.result())






test_1_time_start = time.perf_counter()
asyncio.run(test1())
test_1_time_end = time.perf_counter()
print(f"Total time for test 1 is {test_1_time_end - test_1_time_start}")
