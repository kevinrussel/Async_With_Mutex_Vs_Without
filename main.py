import asyncio
import aiohttp
import time
import requests
import csv
import threading
import queue

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
    try:
        r = requests.get(url, timeout=10)
        return r.status_code
    except requests.RequestException as e:
        return f"ERROR: {e}"


def test_2(num_of_files, file_name, data_file):
    with open(data_file,'r') as file:
        lines = file.readlines()
    result = []
    counter = 0
    for line in lines:
        if(counter >= num_of_files):
            break
        result.append((line,test_2_get_header(line.strip())))
        counter +=1
    
    with open(file_name, "w") as file2:
        for value in result:
            file2.write(f"{value[0].strip()} -> {value[1]}\n")


def test_3(num_of_files,file_name,data_file):
    pass


def get_time():
    return time.perf_counter()



def start_test_1(num_of_files,file_name,data_file):
    
    test_1_time_start = get_time()
    asyncio.run(test1(num_of_files,file_name,data_file))
    test_1_time_end = get_time()
    total_time = test_1_time_end - test_1_time_start
    return total_time


def start_test_2(num_of_files, file_name, data_file):
    test_2_time_start = get_time()
    test_2(num_of_files,file_name,data_file)
    test_2_time_end = get_time()
    total_time = test_2_time_end - test_2_time_start
    return total_time


def start_test_3(num_of_files,file_name,data_file):
    test_3_time_start = get_time()
    test_3(num_of_files,file_name,data_file)
    test_3_end_time = get_time()
    total_time = test_3_end_time - test_3_time_start
    return total_time
    pass

def create_csv_file(filepath):
    with open(filepath,'w',newline='') as csvfile:
        fieldnames = ['Total_Packets','Total_Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def edit_csv_file(csv_filepath, total_num_of_packets, total_time):
    fieldnames = ['Total_Packets', 'Total_Time']
    data = {'Total_Packets': total_num_of_packets, 'Total_Time': total_time}
    with open(csv_filepath, 'a' , newline= '') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writerow(data)

def run_test(num_of_packets,data_file, csv_result_file_path, runs_result_path):
        sequential = False
        threading = False
        if "sequential" in csv_result_file_path:
            sequential = True
        elif "threading" in csv_result_file_path:
            threading= True
        for values in num_of_packets:
            path = runs_result_path + f"_{values}_packets"
            if(sequential):
                test_total_time = start_test_2(values,path,data_file)
            elif(threading):
                test_total_time = start_test_3(values,path,data_file)
            else:
                test_total_time = start_test_1(values,path,data_file)
            print(f" total num of packets: {values} total time {test_total_time}")
            edit_csv_file(csv_result_file_path,values,test_total_time)

def main():
    async_file_path = "async/results/async_results.csv"
    sequential_file_path  = "sequential/results/sequential_results.csv"
    threading_file_path = "threading/results/threading_results.csv"



    async_runs_result_path = "async/runs/async"
    sequential_runs_result_path = "sequential/runs/sequential"
    threading_runs_results_path = "threading/runs/threading"

    create_csv_file(async_file_path)
    create_csv_file(sequential_file_path)
    create_csv_file(threading_file_path)
    data_file = "url/data.txt"
    num_of_packets = [10,50,100,250,500,1000,2500,3500,5000]
    run_test(num_of_packets,data_file,async_file_path,async_runs_result_path)
    run_test(num_of_packets,data_file,sequential_file_path,sequential_runs_result_path)
    run_test(num_of_packets,data_file,threading_file_path,threading_runs_results_path)     
main()

