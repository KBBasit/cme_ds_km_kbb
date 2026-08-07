import requests



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
    valid_modes = ["artlist", "timelinevol", 
                   "timelinevolinfo", "timelinetone", 
                   "timelinesourcecountry", "tonechart"]
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode. Choose from {valid_modes}")


    url = "https://api.gdeltproject.org/api/v2/doc/doc"

    params = {
        "query": query,
        "mode": mode,
        "timespan": f"{timespan_value}{timespan_unit}",
        "format": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()