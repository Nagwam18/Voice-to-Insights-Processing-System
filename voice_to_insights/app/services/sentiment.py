from transformers import pipeline

def sentiment_analysis(transcript: str) -> str:
    sentiment_analyzer = pipeline("sentiment-analysis", device=0)
    result = sentiment_analyzer(transcript)[0]

    if result['label'] == "NEGATIVE":
        return "Frustrated but cooperative"
    elif result['label'] == "POSITIVE":
        return "Satisfied and cooperative"
    else:
        return "Neutral but cooperative"
