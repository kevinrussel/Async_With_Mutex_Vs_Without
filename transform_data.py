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
    "https://linkedin.com",
    "https://microsoft.com",
    "https://apple.com",
    "https://twitch.com",
    "https://discord.com",
    "https://facebook.com",
    "https://tiktok.com",
    "https://bing.com",
    "https://linkedin.com",
    "https://netflix.com",
    "https://pintrest.com",
    "https://fandom.com",
    "https://canva.com",
    "https://spotify.com",
    "https://msn.com",
    "https://imdb.com",
    "https://paypal.com",
    "https://ebay.com",
    "https://openai.com",
    "https://weather.com"
] * 200
    with open("url/data.txt", "w") as file:
        for index in urls:
            file.write(f"{index}\n")

main()