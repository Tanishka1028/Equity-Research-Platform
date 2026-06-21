import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.data_fetcher import get_stock_data
from src.financials import get_financial_metrics
from src.technicals import add_indicators
from src.recommendation import generate_rating
from src.peer_comparison import compare_stocks
from src.valuation import calculate_dcf
from src.report_generator import generate_report
from src.sentiment import get_news_sentiment

st.set_page_config(
    page_title="Equity Research Platform",
    layout="wide"
)

st.title("📈 Equity Research Platform")

st.sidebar.header("Peer Comparison")

peer_input = st.sidebar.text_input(
    "Enter Tickers",
    "AAPL,MSFT,GOOG"
)

ticker = st.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

if st.button("Analyze"):

    (
        info,
        history,
        financials,
        balance_sheet,
        cashflow
    ) = get_stock_data(ticker)

    if history.empty:

        st.error("No stock data found.")
        st.stop()

    history = add_indicators(history)

    metrics = get_financial_metrics(info)

    # --------------------
    # COMPANY OVERVIEW
    # --------------------

    st.header("Company Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Company",
        info.get("longName", "N/A")
    )

    col2.metric(
        "Sector",
        info.get("sector", "N/A")
    )

    col3.metric(
        "Industry",
        info.get("industry", "N/A")
    )

    # --------------------
    # FINANCIAL METRICS
    # --------------------

    st.divider()

    st.header("Financial Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "PE",
        round(metrics["PE"], 2)
        if metrics["PE"]
        else "N/A"
    )

    c2.metric(
        "ROE",
        f"{metrics['ROE']:.2%}"
        if metrics["ROE"]
        else "N/A"
    )

    c3.metric(
        "Profit Margin",
        f"{metrics['Profit Margin']:.2%}"
        if metrics["Profit Margin"]
        else "N/A"
    )

    c4.metric(
        "Revenue Growth",
        f"{metrics['Revenue Growth']:.2%}"
        if metrics["Revenue Growth"]
        else "N/A"
    )

    # --------------------
    # TECHNICAL ANALYSIS
    # --------------------

    st.divider()

    st.header("Technical Analysis")

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=history.index,
            open=history["Open"],
            high=history["High"],
            low=history["Low"],
            close=history["Close"],
            name="Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["SMA50"],
            name="SMA50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["SMA200"],
            name="SMA200"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    rsi_values = history["RSI"].dropna()

    latest_rsi = 50

    if len(rsi_values) > 0:

        latest_rsi = rsi_values.iloc[-1]

        st.metric(
            "Current RSI",
            round(latest_rsi, 2)
        )

    # --------------------
    # RECOMMENDATION
    # --------------------

    rating, score = generate_rating(
        metrics,
        latest_rsi
    )

    st.divider()

    st.header("Recommendation")

    st.metric(
        "Investment Score",
        f"{score}/100"
    )

    if rating == "BUY":

        st.success("BUY")

    elif rating == "HOLD":

        st.warning("HOLD")

    else:

        st.error("SELL")

    # --------------------
    # NEWS SENTIMENT
    # --------------------

    st.divider()

    st.header("📰 News Sentiment")

    news_results, overall_score = get_news_sentiment(
        ticker
    )

    if len(news_results) == 0:

        st.warning(
            "No news available."
        )

    else:

        for article in news_results:

            st.subheader(
                article["title"]
            )

            st.write(
                f"Sentiment: {article['label']}"
            )

            st.write(
                f"Score: {article['score']}"
            )

            st.divider()

        st.subheader(
            f"Overall Sentiment Score: {overall_score}"
        )

    # --------------------
    # DCF VALUATION
    # --------------------

    st.divider()

    st.header("DCF Valuation")

    intrinsic_value = calculate_dcf(
        ticker
    )

    current_price = history[
        "Close"
    ].iloc[-1]

    if intrinsic_value:

        upside = (
            (
                intrinsic_value
                - current_price
            )
            / current_price
        ) * 100

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Price",
            f"${current_price:.2f}"
        )

        col2.metric(
            "Intrinsic Value",
            f"${intrinsic_value:.2f}"
        )

        col3.metric(
            "Upside %",
            f"{upside:.2f}%"
        )

    else:

        upside = 0

        st.warning(
            "Unable to calculate DCF"
        )

    # --------------------
    # PDF REPORT
    # --------------------

    st.divider()

    st.header("📄 Research Report")

    if intrinsic_value:

        if st.button(
            "Generate PDF Report"
        ):

            report_file = generate_report(
                ticker=ticker,
                company=info.get(
                    "longName",
                    ticker
                ),
                metrics=metrics,
                current_price=current_price,
                intrinsic_value=intrinsic_value,
                upside=upside,
                rating=rating
            )

            with open(
                report_file,
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="📥 Download Report",
                    data=pdf_file,
                    file_name=report_file,
                    mime="application/pdf"
                )

    # --------------------
    # FINANCIAL STATEMENTS
    # --------------------

    st.divider()

    st.header("Income Statement")
    st.dataframe(financials)

    st.header("Balance Sheet")
    st.dataframe(balance_sheet)

    st.header("Cash Flow Statement")
    st.dataframe(cashflow)

# --------------------
# PEER COMPARISON
# --------------------

st.divider()

st.header("📊 Peer Comparison")

peer_list = [
    x.strip()
    for x in peer_input.split(",")
]

comparison_df = compare_stocks(
    peer_list
)

if comparison_df.empty:

    st.warning(
        "No comparison data available."
    )

else:

    st.dataframe(
        comparison_df,
        use_container_width=True
    )