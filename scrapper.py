# scrapper.py
import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url):
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None, None
        soup = BeautifulSoup(res.text, "html.parser")

        # Extract the title
        title_tag = soup.find("h1", {"id": "firstHeading"})
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Extract main content paragraphs
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return title, None
        paragraphs = content_div.find_all("p")
        content_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return title, content_text if content_text else None

    except Exception as e:
        print("Scraping error:", str(e))
        return None, None
