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

def interest_rate(spot, future, maturity):
    current_date = datetime.now()
    maturity_date = datetime.strptime(maturity, '%Y%m%d')
    difference = abs((maturity_date - current_date).days)
    interest_rate = (future/spot) - 1 
    nominal_annual_rate = round(( interest_rate * (365 / difference) ) * 100, 2)
    return nominal_annual_rate

def search_arbitrage_oportunity(cache):
    if(cache["lowest_ask_interest_rate"] < cache["highest_bid_interest_rate"]):
        print("Oportunidad de arbitraje tomando en", cache["lair_ticker"], "y colocando en", cache["hbir_ticker"])
    else:
        print("No hay oportunidad de arbitraje")

def search_interest_rates(interest_rates):
    lair_result = {
        "lair": None,
        "lair_ticker": None,
        "hbir": None,
        "hbir_ticker": None
    }

    for ticker, data in interest_rates.items():
        ask_interest_rate = data["ask_interest_rate"]
        bid_interest_rate = data["bid_interest_rate"]

        if(lair_result["lair"] is None or lair_result["lair"] > ask_interest_rate):
            lair_result["lair"] = ask_interest_rate
            lair_result["lair_ticker"] = ticker
        if(lair_result["hbir"] is None or lair_result["hbir"] < bid_interest_rate):
            lair_result["hbir"] = bid_interest_rate
            lair_result["hbir_ticker"] = ticker

    return lair_result