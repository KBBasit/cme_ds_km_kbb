import requests
import time
from bs4 import BeautifulSoup


def fetch_data(query, mode="artlist", timespan="3m"):
    """
    Fetches data from the GDELT API based on the provided query, mode and timeframe.
    Args:
        query (str): The search query to fetch data for.
        mode (str): The mode of data to fetch (e.g. articles, timeline volume).
        timespan (str): The timeframe for the data fetch (e.g., "3m" for 3 months).
    Returns:
        json: The JSON response from the GDELT API.
    """
    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": query,
        "mode": mode,
        "timespan": timespan,
        "format": "json"
    }

    for attempt in range(3):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")          

    raise Exception("Failed to fetch data from GDELT API after 3 attempts")


def find_scrapeable_articles(fetched_article_list):
    '''
    From the article list requested from GDELT, find which articles can be scraped.
    Args:
        fetched_article_list (list): The article list requested from GDELT.
    Returns:
        list: A list of the articles from the GDELT request that can be scraped
    '''
    articles_to_scrape = []

    for url in fetched_article_list:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text , "lxml")
            articles_to_scrape.append(url)
        except requests.exceptions.RequestException
            continue

    return articles_to_scrape