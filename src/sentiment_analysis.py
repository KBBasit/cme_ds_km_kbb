from transformers import pipeline



def sentiment_analysis(text_list):
    """
    Perform sentiment analysis on the given text using a pre-trained model.
    Args:
        text_list (list): A list of input texts to analyze.
    Returns:
        list: A list of dictionaries containing the sentiment labels and scores.
    """
    # Load the sentiment analysis pipeline
    sentiment_analyser = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    results = []
    for text in text_list:
        result = sentiment_analyser(text[:500])
        results.append(result[0])

    return results