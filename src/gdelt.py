import requests
import time

# CONSTANTS
DOC_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
VALID_MODES = {"artlist"}
MAX_RECORDS = 250


def fetch_data(query: str,
               mode: str = "artlist",
               timespan: str = "3m",
               num_attempts: int = 3,
               timeout: float = 30,
               max_records: int = MAX_RECORDS
               ):
    """
    Fetches data from the GDELT API based on the provided query, mode and timeframe.
    Args:
        query (str): The search query to fetch data for.
        mode (str): The mode of data to fetch (e.g. articles, timeline volume).
        timespan (str): The timeframe for the data fetch (e.g., "3m" for 3 months).
        num_attemps (int): Number of times to try for a successful request
        timeout (float): Number of seconds before forcefully ending the request
        max_records (int): Maximum number of records to retrieve per request
    Returns:
        json: The JSON response from the GDELT API.
    """

    if mode not in VALID_MODES:
        raise ValueError("ValueError: Invalid mode entered")

    max_records = 250 if max_records > 250 else max_records

    params = {
        "query": query,
        "mode": mode,
        "timespan": timespan,
        "maxrecords": max_records,
        "format": "json"
    }

    for attempt in range(num_attempts):
        try:
            response = requests.get(DOC_API_URL, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.JSONDecodeError as json_error:
            print(f"Attempt {attempt + 1} failed: {json_error}")
            print(response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            print(response.status_code)
        if attempt < (num_attempts - 1):
            sleep_for = 5*(attempt + 1)
            time.sleep(sleep_for)      

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