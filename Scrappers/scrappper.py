from flask import Flask, jsonify, request
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
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
    base_html = requests.get(base_url, headers=headers).text
    base_soup = BeautifulSoup(base_html, "html.parser")

    information = ""
    links = re.findall(r'href\s*=\s*["\'](.*?)["\']', base_html, re.IGNORECASE)

    for link in sorted(set(links)):
        if link.startswith("https://www.hindustantimes.com/") and link.endswith(".html"):
            try:
                html = requests.get(link, headers=headers, timeout=10).text
                soup = BeautifulSoup(html, "html.parser")
                page_str = str(soup)

                match = re.search(r'"articleBody"\s*:\s*"([^"]+)"', page_str)
                if match:
                    article_body = match.group(1)
                    article_body = (
                        article_body.replace('\\"', '"')
                        .replace('\\n', '\n')
                        .strip()
                    )
                    information += f"link: {link}\nArticle information: {article_body}\n\n"
                    print("Extracted:", link)
                else:
                    print("articleBody not found for:", link)
            except Exception as e:
                print("Error fetching:", link, "-", e)

    return information or "No articles found."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
