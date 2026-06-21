import yfinance as yf
from textblob import TextBlob


def get_news_sentiment(ticker):

    try:

        stock = yf.Ticker(ticker)

        news = stock.news

        if not news:

            return [], 0

        news_results = []

        total_score = 0

        count = 0

        for article in news[:10]:

            # Yahoo Finance sometimes stores title differently
            title = article.get("title")

            if not title:

                title = (
                    article.get("content", {})
                    .get("title", "No Title Available")
                )

            sentiment = TextBlob(
                title
            ).sentiment.polarity

            total_score += sentiment

            count += 1

            if sentiment > 0:

                label = "Positive"

            elif sentiment < 0:

                label = "Negative"

            else:

                label = "Neutral"

            news_results.append({

                "title": title,

                "score": round(
                    sentiment,
                    2
                ),

                "label": label

            })

        overall_score = round(
            total_score / count,
            2
        )

        return (
            news_results,
            overall_score
        )

    except Exception as e:

        print(
            f"Sentiment Error: {e}"
        )

        return [], 0