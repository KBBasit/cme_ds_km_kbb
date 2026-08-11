import requests
import time
from bs4 import BeautifulSoup



def find_scrapeable_articles(url_list):
    '''
    From a list of URLs, find which are able to be scraped
    Args:
        fetched_article_list (list): A list of URLs
    Returns:
        list: A filtered list of URLs for websites that can be scraped
    '''
    articles_to_scrape = []

    for url in url_list:
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


def scrape_articles(url_list):
    '''
    From a list of URLs, check which articles can be scraped,
    and scrape bodies of text from each website
    Args:
        url_list: A list of URLs to scrape
    Returns:
        list: A list with entries of text from the scraped websites
    '''
    articles_to_scrape = find_scrapeable_articles(url_list)
    article_texts = []

    for url in articles_to_scrape:
        response = requests.get(url, timeout = 15)
        soup = BeautifulSoup(response.text, "lxml")

        paragraphs = soup.find_all("p")

        for i, paragraph in enumerate(paragraphs):
            paragraphs[i] = paragraph.get_text(" ", strip=True)

        article_text = "\n".join(paragraphs)
        
        article_texts.append(article_text)

    return article_texts