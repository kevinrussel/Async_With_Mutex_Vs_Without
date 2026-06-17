import asyncio
import aiohttp
import time

async def test1():
    pass
test_1_time_start = time.time()
asyncio.run(test1())
test_1_time_end = time.time()
print(f"Total time for test 1 is {test_1_time_end - test_1_time_start}")
