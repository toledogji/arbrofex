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

#Calculo la diferencia entre la fecha de vencimiento del instrumento y la fecha actual
def date_diff(maturity_date):
    current_date = datetime.now()
    maturity_date = datetime.strptime(maturity_date, '%Y%m%d')
    difference = abs((maturity_date - current_date).days)
    return difference

#Calcula la tasa de interes en base al precio spot, futuro y la diferencia al vencimiento del instrumento.
def calculate_interest_rate(spot, future, difference):
    """
    Calcula la tasa de interes implicita.
    
    >>> calculate_interest_rate(100,105,30)
    60.83
    
    """
    interest_rate = (future/spot) - 1 
    nominal_annual_rate = round(( interest_rate * (365 / difference) ) * 100, 2)
    return nominal_annual_rate

#Obtiene la tasa de interes para el instrumento
def get_interest_rate(spot, future, maturity):
    difference = date_diff(maturity)
    interest_rate = calculate_interest_rate(spot, future, difference)
    return interest_rate

#Evalua si hay una oportunidad de arbitraje 
def search_arbitrage_oportunity(ir_cache):
    if(ir_cache["lowest_ask_interest_rate"] < ir_cache["highest_bid_interest_rate"]):
        print("Oportunidad de arbitraje tomando en", ir_cache["lair_ticker"], "al", ir_cache["lowest_ask_interest_rate"], 
                "y colocando en", ir_cache["hbir_ticker"], "al", ir_cache["highest_bid_interest_rate"])
    else:
        print("No hay oportunidad de arbitraje")

#Busca dentro de diccionario donde estan las tasas de interes por cada instrumento, las tasas de interes más convenientes.
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

#Actualiza el lowest ask interest rate en la cache
def update_lair_cache(ir_cache, ask_interest_rate, symbol, interest_rates):
    """
    Actualiza el lowest ask interest rate en la cache.
    
    >>> update_lair_cache({"lowest_ask_interest_rate" : 34.38,"lair_ticker": "GGAL/FEB22","highest_bid_interest_rate" : 32,"hbir_ticker": "PAMP/FEB22"},35,"GGAL/FEB22", {'GGAL/FEB22': {'ask_interest_rate': 35, 'bid_interest_rate': None}, 'YPFD/FEB22': {'ask_interest_rate': 37.03, 'bid_interest_rate': 30.36}, 'DLR/FEB22': {'ask_interest_rate': 55.63, 'bid_interest_rate': None}, 'PAMP/FEB22': {'ask_interest_rate': 36, 'bid_interest_rate': 33}})
    {'lowest_ask_interest_rate': 35, 'lair_ticker': 'GGAL/FEB22', 'highest_bid_interest_rate': 32, 'hbir_ticker': 'PAMP/FEB22'}
    
    """
    if(ir_cache["lowest_ask_interest_rate"] is None 
            or ir_cache["lowest_ask_interest_rate"] > ask_interest_rate ):
            ir_cache["lowest_ask_interest_rate"] = ask_interest_rate
            ir_cache["lair_ticker"] = symbol
            
    if( ir_cache["lair_ticker"] == symbol and 
        ir_cache["lowest_ask_interest_rate"] < ask_interest_rate):
        irates_result = search_interest_rates(interest_rates)
        ir_cache["lowest_ask_interest_rate"] = irates_result["lair"]
        ir_cache["lair_ticker"] = irates_result["lair_ticker"]
        
    return ir_cache

#Actualiza el highest bid interest rate en la cache
def update_hbir_cache(ir_cache, bid_interest_rate, symbol, interest_rates):
    """
    Actualiza el highest bid interest rate en la cache.
    
    >>> update_hbir_cache({"lowest_ask_interest_rate" : 34.38,"lair_ticker": "GGAL/FEB22","highest_bid_interest_rate" : 32,"hbir_ticker": "PAMP/FEB22"},31.3,"PAMP/FEB22", {'GGAL/FEB22': {'ask_interest_rate': None, 'bid_interest_rate': None}, 'YPFD/FEB22': {'ask_interest_rate': 37.03, 'bid_interest_rate': 30.36}, 'DLR/FEB22': {'ask_interest_rate': 55.63, 'bid_interest_rate': None}, 'PAMP/FEB22': {'ask_interest_rate': 34.38, 'bid_interest_rate': 31.3}})
    {'lowest_ask_interest_rate': 34.38, 'lair_ticker': 'GGAL/FEB22', 'highest_bid_interest_rate': 31.3, 'hbir_ticker': 'PAMP/FEB22'}
    
    """
    if( ir_cache["highest_bid_interest_rate"] is None 
            or ir_cache["highest_bid_interest_rate"] < bid_interest_rate):
            ir_cache["highest_bid_interest_rate"] = bid_interest_rate
            ir_cache["hbir_ticker"] = symbol

    if( ir_cache["hbir_ticker"] == symbol and
        ir_cache["highest_bid_interest_rate"] > bid_interest_rate):
        irates_result = search_interest_rates(interest_rates)
        ir_cache["highest_bid_interest_rate"] = irates_result["hbir"]
        ir_cache["hbir_ticker"] = irates_result["hbir_ticker"]
        
    return ir_cache

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)