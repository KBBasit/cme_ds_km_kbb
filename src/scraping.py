import requests
import time
from bs4 import BeautifulSoup



def scrape_articles(url_list):
    '''
    From a list of URLs, check which websites can be scraped,
    and scrape bodies of text from each website
    Args:
        url_list (list): A list of URLs to validate and scrape
    Returns:
        list: A list of dictionaries containing the URL and the scraped text for each valid article
    '''
    article_texts = []

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
        paragraphs = [paragraph.get_text(" ", strip=True)
                      for paragraph in soup.find_all("p")]

        article_text = "\n".join(paragraphs)
        
        if len(article_text) > 500:
            article_texts.append({'url': url, 
                                  'text': article_text})

    return article_texts