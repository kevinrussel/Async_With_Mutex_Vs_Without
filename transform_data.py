import time

def main():
    with open("url.txt", "r") as file:
        lines = file.readlines()
    
    print(lines[0].split(","))
    with open("data.txt", "a") as file:

        for line in lines:
            postfix = line.split(",")[1]
          
            url = "https://"+postfix
            
            file.write(url)
            

main()