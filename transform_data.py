import time

def main():
    with open("url.txt", "r") as file:
        lines = file.readlines()
    
    print(lines[0].split(","))

    for line in lines:
        postfix = line.split(",")[1]
        print(postfix)
        time.sleep(5)

main()