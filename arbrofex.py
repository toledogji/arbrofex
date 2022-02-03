import pyRofex
import remarket_auth as ra
import yfinance as yf
import market_operations as mo
from instruments import instruments
from datetime import datetime


pyRofex.initialize(user=ra.USER,
                   password=ra.PASSWORD,
                   account=ra.ACCOUNT,
                   environment=pyRofex.Environment.REMARKET)

ir_cache = {
    "lowest_ask_interest_rate" : None,
    "lair_ticker": None,
    "highest_bid_interest_rate" : None,
    "hbir_ticker": None,
}

interest_rates = {}
# Handlers para procesar los mensajes y excepciónes.

def market_data_handler(message):
    #Extraigo los datos que vienen en el mensaje
    symbol = message["instrumentId"]["symbol"]
    maturity = pyRofex.get_instrument_details(symbol)["instrument"]["maturityDate"]
    bid_price = None
    ask_price = None
    if(message["marketData"]["BI"] and message["marketData"]["BI"] != None):
        bid_price = message["marketData"]["BI"][0]["price"]
    if(message["marketData"]["OF"] and message["marketData"]["BI"] != None):
        ask_price = message["marketData"]["OF"][0]["price"]

    #Printeo los datos para visualizarlos
    print("Ticker:", symbol)
    #print("Maturity:", maturity)
    if(bid_price is not None):
        print("BID: ", bid_price)
    if(ask_price is not None):
        print("ASK: ", ask_price)
    
    #Obtengo el precio spot de cada uno de los instrumentos
    spot_price = mo.get_spot_price(instruments[symbol])
    print("SPOT:", spot_price)

    interest_rates[symbol] = {
        "ask_interest_rate": None,
        "bid_interest_rate": None,
    }
    #Calculo las tasa de interes implicitas
   
    if(ask_price is not None):
        ask_interest_rate = mo.get_interest_rate(spot_price, ask_price, maturity)
        interest_rates[symbol]["ask_interest_rate"] = ask_interest_rate

        if(ir_cache["lowest_ask_interest_rate"] is None 
            or ir_cache["lowest_ask_interest_rate"] > ask_interest_rate ):
            ir_cache["lowest_ask_interest_rate"] = ask_interest_rate
            ir_cache["lair_ticker"] = symbol
            
        if( ir_cache["lair_ticker"] == symbol and 
            ir_cache["lowest_ask_interest_rate"] < ask_interest_rate):
            irates_result = mo.search_interest_rates(interest_rates)
            ir_cache["lowest_ask_interest_rate"] = irates_result["lair"]
            ir_cache["lair_ticker"] = irates_result["lair_ticker"]

        print("TASA IMPLICITA TOMADORA:", ask_interest_rate, '%')
        
    if(bid_price is not None):
        bid_interest_rate = mo.get_interest_rate(spot_price, bid_price, maturity)
        interest_rates[symbol]["bid_interest_rate"] = bid_interest_rate

        if( ir_cache["highest_bid_interest_rate"] is None 
            or ir_cache["highest_bid_interest_rate"] < bid_interest_rate):
            ir_cache["highest_bid_interest_rate"] = bid_interest_rate
            ir_cache["hbir_ticker"] = symbol

        if( ir_cache["hbir_ticker"] == symbol and
            ir_cache["highest_bid_interest_rate"] > bid_interest_rate):
            irates_result = mo.search_interest_rates(interest_rates)
            ir_cache["highest_bid_interest_rate"] = irates_result["hbir"]
            ir_cache["hbir_ticker"] = irates_result["hbir_ticker"]

        print("TASA IMPLICITA COLOCADORA:", bid_interest_rate, "%")
    mo.search_arbitrage_oportunity(ir_cache)

def error_handler(message):
    print("Error Message Received: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))

# Conexión websocket
pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)

# Lista de instrumentos a suscribir
tickers = ["GGAL/FEB22", "PAMP/FEB22", "YPFD/FEB22", "DLR/FEB22"]

# Defino a que datos me voy a suscribir
entries = [pyRofex.MarketDataEntry.BIDS,
           pyRofex.MarketDataEntry.OFFERS,
           pyRofex.MarketDataEntry.LAST]

# Recibo datos del mercado
pyRofex.market_data_subscription(tickers=tickers,
                                 entries=entries)
