import yfinance as yf

def get_stock_data(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    history = stock.history(period="5y")

    financials = stock.financials 
    
    balance_sheet = stock.balance_sheet

    cashflow = stock.cashflow


    return (
        info, 
        history,
        financials,
        balance_sheet,
        cashflow
    )
