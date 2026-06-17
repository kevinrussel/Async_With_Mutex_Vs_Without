import asyncio
import aiohttp
import time


async def test1_url(session,url, semaphore):
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
    semaphore = asyncio.Semaphore(10)
    resolver = aiohttp.AsyncResolver(nameservers=["8.8.8.8", "8.8.4.4"])
    connector = aiohttp.TCPConnector(
    resolver=resolver,
    limit=10,
    ttl_dns_cache=300,  # cache DNS results for 5 minutes
    use_dns_cache=True  # don't re-lookup same domain
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        responses = []
        with open('data.txt', 'r') as file:
            lines = file.readlines()
        async with asyncio.TaskGroup() as tg:
            for line in lines:
                task = tg.create_task(test1_url(session,line, semaphore))
                responses.append(task)


   
    with open("answer.txt", "w") as file:
        for value in responses:
            values = value.result()
            file.write(f"{values[0]}->{values[1]}\n")






test_1_time_start = time.perf_counter()
asyncio.run(test1())
test_1_time_end = time.perf_counter()
print(f"Total time for test 1 is {test_1_time_end - test_1_time_start}")
