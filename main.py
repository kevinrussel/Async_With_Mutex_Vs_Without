import asyncio
import aiohttp
import time
import requests

mutex = asyncio.Lock()


async def test1_url(session,url, semaphore):
    async with semaphore:
        try:
            async with session.get(url,
                                timeout = aiohttp.ClientTimeout(total=3),
                                ssl=False) as response:
                status = response.status
                return (url,status)
        except OSError:
            return url, "OS ERROR"
        except aiohttp.ClientConnectorDNSError:
            return url, "DNS FAILED"      
        except aiohttp.ClientConnectorError:
            return url, "CONNECTION FAILED"
        except asyncio.TimeoutError:
            return url, "TIMEOUT"
        except Exception as e:
            return url, f"FAILED: {type(e).__name__}" 


async def test1():
    semaphore = asyncio.Semaphore(25)
    resolver = aiohttp.AsyncResolver(nameservers=["8.8.8.8", "8.8.4.4"])
    connector = aiohttp.TCPConnector(
    resolver=resolver,
    limit=25,
    ttl_dns_cache=300,  # cache DNS results for 5 minutes
    use_dns_cache=True  # don't re-lookup same domain
    )
    
    async with aiohttp.ClientSession(connector=connector) as session:
        responses = []
        with open('data.txt', 'r') as file:
            lines = file.readlines()
        tasks = [test1_url(session, line.strip(), semaphore) for line in lines]
        responses = await asyncio.gather(*tasks, return_exceptions=True)


   
    with open("answer.txt", "w") as file:
        for value in responses:
            file.write(f"{value[0]} -> {value[1]}\n")






test_1_time_start = time.perf_counter()
asyncio.run(test1())
test_1_time_end = time.perf_counter()
print(f"Total time for test 1 is {test_1_time_end - test_1_time_start}")


def get_header(url):
    r = requests.get(url)
    return r.status_code


def test_2():
    with open("data.txt",'r') as file:
        lines = file.readlines()
    result = []
    for line in lines:
        result.append((line,get_header(line.strip())))
    
    with open("sequential_requests.txt", "w") as file2:
        for value in result:
            file.write(f"{value[0]} -> {value[1]}\n")








# time_2_time_start = time.perf_counter()







test_2()