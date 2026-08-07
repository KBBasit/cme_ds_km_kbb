import requests



def fetch_articles(query, timespan_unit = "m", timespan_value = 3):
    """
    Fetches articles from the GDELT API based on the provided query.
    Args:
        query (str): The search query to fetch articles for.
        timespan_unit (str): The unit of the timespan (e.g., "m" for minutes, "h" for hours).
        timespan_value (int): The value of the timespan.
    Returns:
        list: A list of articles matching the query.
    """
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query,
        "mode": "artlist",
        "timespan": f"{timespan_value}{timespan_unit}",
        "format": "json"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return "No articles found or an error occurred while fetching articles."