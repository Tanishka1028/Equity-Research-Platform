import yfinance as yf


def calculate_dcf(ticker):

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        cashflow = stock.cashflow

        if cashflow.empty:
            return None

        # Free Cash Flow
        if "Free Cash Flow" in cashflow.index:

            fcf = cashflow.loc["Free Cash Flow"].iloc[0]

        else:
            return None

        growth_rate = 0.08
        discount_rate = 0.10
        terminal_growth = 0.03

        projected_fcf = []

        current_fcf = fcf

        for year in range(1, 6):

            current_fcf *= (1 + growth_rate)

            projected_fcf.append(current_fcf)

        present_value = 0

        for i, cash in enumerate(projected_fcf, start=1):

            present_value += cash / ((1 + discount_rate) ** i)

        terminal_value = (
            projected_fcf[-1]
            * (1 + terminal_growth)
        ) / (discount_rate - terminal_growth)

        terminal_pv = terminal_value / (
            (1 + discount_rate) ** 5
        )

        enterprise_value = (
            present_value
            + terminal_pv
        )

        shares = info.get(
            "sharesOutstanding"
        )

        if not shares:

            return None

        intrinsic_value = (
            enterprise_value
            / shares
        )

        return round(
            intrinsic_value,
            2
        )

    except:

        return None