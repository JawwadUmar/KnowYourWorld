from flask import Flask
import requests
import re
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

@app.route("/extract", methods=["GET"])
def extract():
    base_url = "https://www.hindustantimes.com"
    homePage = requests.get(base_url, headers=HEADERS).text

    information = ""
    categories = set()
    links = [a["href"] for a in BeautifulSoup(homePage, "html.parser").find_all("a", href=True)]

    for link in sorted(set(links)):
        if link.startswith("https://www.hindustantimes.com/") and link.endswith(".html"):
            path = urlparse(link).path
            category = path.strip("/").split("/")[0]
            categories.add(category)
            if(category != "world-news" and category != "india-news" and category != "sports"):
                continue
            try:
                htmlPageResponse = requests.get(link, headers=HEADERS, timeout=10)
                htmlPageText:str = htmlPageResponse.text
                soup = BeautifulSoup(htmlPageText, "html.parser")
                
                for script in soup.find_all("script", type="application/ld+json"):
                    try:
                        data = json.loads(script.string)
                        if "articleBody" in data:
                            print("Extracted:", link)
                            article_body = data["articleBody"]
                            information += f"link: {link}\nArticle information: {article_body}\n\n"
                            break
                    except Exception as e:
                        pass
            except Exception as e:
                print("Error fetching:", link, "-", e)
    
    with open("articles.txt", "w", encoding="utf-8") as file:
        file.write(information)

    with open("categories.txt", "w", encoding="utf-8") as file:
        for category in sorted(categories):
            file.write(category + "\n")

    return information or "No articles found."


if __name__ == "__main__":
    extract()
    # app.run(host="0.0.0.0", port=8000)
    # extract()
