import asyncio
import aiohttp
import time
semaphore = asyncio.Semaphore(50)
async def test1_url(session,url):
    async with semaphore:
        try:
            async with session.get(url,
                                timeout = aiohttp.ClientTimeout(total=3),
                                ssl=False) as response:
                status = response.status
                return (url,status)
        except aiohttp.ClientConnectorDNSError:
            return url, "DNS FAILED"      
        except aiohttp.ClientConnectorError:
            return url, "CONNECTION FAILED"
        except asyncio.TimeoutError:
            return url, "TIMEOUT"
        except Exception as e:
            return url, f"FAILED: {type(e).__name__}" 


async def test1():
    async with aiohttp.ClientSession() as session:
        responses = []
        with open('data.txt', 'r') as file:
            lines = file.readlines()
        async with asyncio.TaskGroup() as tg:
            for line in lines:
                task = tg.create_task(test1_url(session,line))
                responses.append(task)


   
    with open("answer.txt", "w") as file:
        for value in responses:
            values = value.result()
            file.write(f"{values[0]}->{values[1]}\n")






test_1_time_start = time.perf_counter()
asyncio.run(test1())
test_1_time_end = time.perf_counter()
print(f"Total time for test 1 is {test_1_time_end - test_1_time_start}")
