import yfinance as yf
import pandas as pd


def compare_stocks(tickers):

    results = []

    for ticker in tickers:

        try:

            stock = yf.Ticker(ticker)

            info = stock.info

            results.append({

                "Ticker": ticker,

                "Company":
                info.get("longName", "N/A"),

                "Sector":
                info.get("sector", "N/A"),

                "Industry":
                info.get("industry", "N/A"),

                "PE":
                info.get("trailingPE", 0),

                "Forward PE":
                info.get("forwardPE", 0),

                "Market Cap":
                info.get("marketCap", 0),

                "Dividend Yield":
                info.get("dividendYield", 0),

                "Beta":
                info.get("beta", 0)

            })

        except Exception as e:

            print(f"Error with {ticker}: {e}")

    return pd.DataFrame(results)