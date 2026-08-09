import requests
import time



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

        except requests.exceptions.HTTPError:
            print(f"Attempt {attempt + 1}")
            print(f"Status code: {response.status_code}")
            print(response.text[:500])            

    raise Exception("Failed to fetch data from GDELT API after 3 attempts")


def articles_allowing_scraping(fetched_article_list):
    '''
    From the article list requested from GDELT, find which articles can be scraped.
    Args:
        fetched_article_list (list): The article list requested from GDELT.
    Returns:
        list: A list of the articles from the GDELT request that can be scraped
    '''
    return 