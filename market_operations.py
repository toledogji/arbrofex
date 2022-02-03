import pyRofex
import yfinance as yf
from datetime import datetime

def get_bid(ticker):
    ticker_data = pyRofex.get_market_data(
        ticker=ticker,
        entries=[pyRofex.MarketDataEntry.BIDS]
    ) 
    return ticker_data["marketData"]["BI"][0]["price"]

def get_ask(ticker):
    ticker_data = pyRofex.get_market_data(
        ticker=ticker,
        entries=[pyRofex.MarketDataEntry.OFFERS]
    ) 
    return ticker_data["marketData"]["OF"][0]["price"]

def get_spot_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

def date_diff(maturity_date):
    current_date = datetime.now()
    maturity_date = datetime.strptime(maturity_date, '%Y%m%d')
    difference = abs((maturity_date - current_date).days)
    return difference

def calculate_interest_rate(spot, future, difference):
    """
    Calcula la tasa de interes implicita.
    
    >>> calculate_interest_rate(100,105,30)
    60.83
    
    """
    interest_rate = (future/spot) - 1 
    nominal_annual_rate = round(( interest_rate * (365 / difference) ) * 100, 2)
    return nominal_annual_rate

def get_interest_rate(spot, future, maturity):
    difference = date_diff(maturity)
    interest_rate = calculate_interest_rate(spot, future, difference)
    return interest_rate

def search_arbitrage_oportunity(ir_cache):
    if(ir_cache["lowest_ask_interest_rate"] < ir_cache["highest_bid_interest_rate"]):
        print("Oportunidad de arbitraje tomando en", ir_cache["lair_ticker"], "al", ir_cache["lowest_ask_interest_rate"], 
                "y colocando en", ir_cache["hbir_ticker"], "al", ir_cache["highest_bid_interest_rate"])
    else:
        print("No hay oportunidad de arbitraje")

def search_interest_rates(interest_rates):
    ir_result = {
        "lair": None,
        "lair_ticker": None,
        "hbir": None,
        "hbir_ticker": None
    }

    for ticker, data in interest_rates.items():
        ask_interest_rate = data["ask_interest_rate"]
        bid_interest_rate = data["bid_interest_rate"]
        if(ir_result["lair"] is None or (ask_interest_rate is not None and ir_result["lair"] > ask_interest_rate)):
            ir_result["lair"] = ask_interest_rate
            ir_result["lair_ticker"] = ticker
        if(ir_result["hbir"] is None or (bid_interest_rate is not None and ir_result["hbir"] < bid_interest_rate)):
            ir_result["hbir"] = bid_interest_rate
            ir_result["hbir_ticker"] = ticker
    return ir_result

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)