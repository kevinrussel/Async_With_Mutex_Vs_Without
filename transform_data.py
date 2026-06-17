import time

def main():
    with open("url.txt", "r") as file:
        lines = file.readlines()
    
    print(lines[0])
    time.sleep(5)