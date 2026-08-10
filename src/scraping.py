import requests
import time
from bs4 import BeautifulSoup



def find_scrapeable_articles(fetched_article_list):
    '''
    From the article list requested from GDELT, find which articles can be scraped.
    Args:
        fetched_article_list (list): The article list requested from GDELT.
    Returns:
        list: A list of the articles from the GDELT request that can be scraped
    '''
    articles_to_scrape = []

    for article in fetched_article_list:
        url = article["url"]
        # Check if article can be reached
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            continue

        # Check if content type is HTML
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            continue

        # Can it be parsed
        try:
            soup = BeautifulSoup(response.text, "lxml")
        except Exception:
            continue

        # Does the parsed page contain meaningful text
        paragraphs = soup.find_all("p")

        for i, paragraph in enumerate(paragraphs):
            paragraphs[i] = paragraph.get_text(" ", strip=True)

        article_text = "\n".join(paragraphs)
        
        if len(article_text) > 500:
            articles_to_scrape.append(url)

    return articles_to_scrape