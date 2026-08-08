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
        response = requests.get(url, params=params)

        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying in 5 seconds... (Attempt {attempt + 1}/3)")
            time.sleep(5)
            continue

        response.raise_for_status()
        return response.json()

    raise Exception("Failed to fetch data from GDELT API after 3 attempts")