import time

def main():
    with open("url.txt", "r") as file:
        lines = file.readlines()
    
    print(lines[0].split(","))
    counter = 0
    with open("data.txt", "a") as file:
        for line in lines:
            if ( counter > 300):
                break
            postfix = line.split(",")[1]
            url = "https://"+postfix
            file.write(url)
            counter +=1

main()