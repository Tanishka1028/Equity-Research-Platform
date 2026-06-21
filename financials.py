def get_financial_metrics(info):

    metrics = {

        "PE": 
        info.get("trailingPE"),

        "ROE": 
        info.get("returnOnEquity"),

        "Profit Margin": 
        info.get("profitMargins"),

        "Revenue Growth": 
        info.get("revenueGrowth"),
        "Market Cap":
        info.get("marketCap")

    }

    return metrics