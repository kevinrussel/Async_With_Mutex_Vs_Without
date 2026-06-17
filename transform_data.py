import time

def main():
    # with open("url.txt", "r") as file:
    #     lines = file.readlines()
    
    # print(lines[0].split(","))
    # counter = 0
    # with open("data.txt", "a") as file:
    #     for line in lines:
    #         if ( counter > 300):
    #             break
    #         postfix = line.split(",")[1]
    #         url = "https://"+postfix
    #         file.write(url)
    #         counter +=1

    urls = [
    "https://google.com",
    "https://github.com",
    "https://wikipedia.org",
    "https://amazon.com",
    "https://reddit.com",
    "https://youtube.com",
    "https://twitter.com",
    "https://linkedin.com",
    "https://microsoft.com",
    "https://apple.com"
] * 50
    with open("data.txt", "w") as file:
        for index in urls:
            file.write(f"{index}\n")

main()