import threading
import requests
import queue

def start_worker():
    pass


def main():
    max_workers = 8
    threads = []

    for _ in range(max_workers):
        threads.append(threading.Thread(target=start_worker))
    for value in threads:
        value.start()