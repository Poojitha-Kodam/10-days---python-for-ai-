def classify_sentiment(text: str) -> str:
    text = text.lower()
    if "good" in text or "great" in text or "happy" in text:
        return "positive"
    elif "bad" in text or "sad" in text or "angry" in text:
        return "negative"
    else:
        return "neutral"

msgs = ["I am feeling good today", "This is a bad day", "I am neutral about this"]  

for msg in msgs:
    sentiment = classify_sentiment(msg)
    print(f"User: {msg} => Sentiment: {sentiment}")


