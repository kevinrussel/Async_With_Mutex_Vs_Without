import asyncio
import aiohttp
import time
import requests
import csv

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


async def test1(num_of_urls_processed,file_name, data_file):
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
        with open(data_file, 'r') as file:
            lines = file.readlines()
        tasks = []
        counter = 0
        for line in lines:
            if(counter >=num_of_urls_processed):
                break
            tasks.append(test1_url(session,line.strip(),semaphore))
            counter +=1
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    with open(file_name, "w") as file:
        for value in responses:
            file.write(f"{value[0]} -> {value[1]}\n")



def test_2_get_header(url):
    r = requests.get(url)
    return r.status_code


def test_2():
    with open("data.txt",'r') as file:
        lines = file.readlines()
    result = []
    for line in lines:
        result.append((line,test_2_get_header(line.strip())))
    
    with open("sequential_requests.txt", "w") as file2:
        for value in result:
            file2.write(f"{value[0].strip()} -> {value[1]}\n")


def get_time():
    return time.perf_counter()



def start_test_1(num_of_files,file_name,data_file):
    
    test_1_time_start = get_time()
    asyncio.run(test1(num_of_files,file_name,data_file))
    test_1_time_end = get_time()
    total_time = test_1_time_end - test_1_time_start
    return total_time
def create_csv_file(filepath):
    with open(filepath,'w',newline='') as csvfile:
        fieldnames = ['Total_Packets','Total_Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def edit_csv_file(csv_filepath, total_num_of_packets, total_time):
    data = {'Total_Packets': total_num_of_packets, 'Total_Time': total_time}
    with open(csv_filepath, 'a' , newline= '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)



def main():
    async_file_path = "async/results/async_results.csv"
    sequential_file_path  = "sequential/results/sequential_results.csv"
    create_csv_file(async_file_path)
    create_csv_file(sequential_file_path)
    data_file = "url/data.txt"
    num_of_packets = [10,100,200,400]
    for values in num_of_packets:
        test_1_total_time = start_test_1(values,f"async/runs/async_{values}_packets",data_file)
        print(f" total num of packets: 10 total time {test_1_total_time}")
        edit_csv_file(async_file_path,values,test_1_total_time)
          
main()

