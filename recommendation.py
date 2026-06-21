def generate_rating(metrics, latest_rsi):

    score = 0

    pe = metrics.get("PE")
    roe = metrics.get("ROE")
    growth = metrics.get("Revenue Growth")
    margin = metrics.get("Profit Margin")

    if pe is not None and pe < 25:
        score += 20

    if roe is not None and roe > 0.15:
        score += 25

    if growth is not None and growth > 0.10:
        score += 25

    if margin is not None and margin > 0.10:
        score += 15

    if latest_rsi < 40:
        score += 15

    if score >= 80:
        return "BUY", score
    elif score >= 50:
        return "HOLD", score
    else:
        return "SELL", score