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
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(5)      

    raise Exception("Failed to fetch data from GDELT API after 3 attempts")


def enrich_scraped_articles(scraped_articles, article_list):
    """
    Enriches the scraped articles with additional metadata from the GDELT API response.
    Args:
        scraped_articles (list): A list of dictionaries containing the URL and the scraped text for each valid article.
        article_list (list): A list of articles from the GDELT API response.
    Returns:
        list: A list of enriched articles with additional metadata.
    """
    enriched_articles = []
    url_to_metadata = {article["url"]: article for article in article_list}

    for article in scraped_articles:
        url = article["url"]
        if url in url_to_metadata:
            metadata = url_to_metadata[url]
            enriched_article = {
                "title": metadata["title"],
                "url": url,
                "gdelt_seendate": metadata["seendate"],
                "language": metadata["language"],
                "source_country": metadata["sourcecountry"],
                "text": article["text"],
            }
            enriched_articles.append(enriched_article)

    return enriched_articles