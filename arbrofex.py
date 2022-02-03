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

#Inicializo el diccionario que me permite guardar las mejores tasas de interes.
ir_cache = {
    "lowest_ask_interest_rate" : None,
    "lair_ticker": None,
    "highest_bid_interest_rate" : None,
    "hbir_ticker": None,
}

#Inicializo el diccinario que guarda todas las tasas de interes
interest_rates = {}

# Handlers para procesar los mensajes y excepciónes.
def market_data_handler(message):
    #Extraigo los datos que vienen en el mensaje
    symbol = message["instrumentId"]["symbol"]
    maturity = pyRofex.get_instrument_details(symbol)["instrument"]["maturityDate"]
    spot_price = mo.get_spot_price(instruments[symbol])
    bid_price = None
    ask_price = None
    #Inicializo el diccionario donde se van a guardar los datos 
    #de las tasas de interes para cada instrumento
    interest_rates[symbol] = {
        "ask_interest_rate": None,
        "bid_interest_rate": None,
    }

    if(message["marketData"]["BI"] and message["marketData"]["BI"] != None):
        bid_price = message["marketData"]["BI"][0]["price"]
    if(message["marketData"]["OF"] and message["marketData"]["BI"] != None):
        ask_price = message["marketData"]["OF"][0]["price"]
    
    #Muestro los datos de insturmento
    print("Ticker:", symbol)
    print("BID: ", bid_price)
    print("ASK: ", ask_price)    
    print("SPOT:", spot_price)

    #Calculo las tasa de interes implicitas
    if(ask_price is not None):
        ask_interest_rate = mo.get_interest_rate(spot_price, ask_price, maturity)
        interest_rates[symbol]["ask_interest_rate"] = ask_interest_rate
        print("TASA IMPLICITA TOMADORA:", ask_interest_rate, '%')

        ir_cache_updated = mo.update_lair_cache(ir_cache, ask_interest_rate, symbol, interest_rates)
        ir_cache.update(ir_cache_updated)
        
    if(bid_price is not None):
        bid_interest_rate = mo.get_interest_rate(spot_price, bid_price, maturity)
        interest_rates[symbol]["bid_interest_rate"] = bid_interest_rate
        print("TASA IMPLICITA COLOCADORA:", bid_interest_rate, "%")

        ir_cache_updated = mo.update_hbir_cache(ir_cache, bid_interest_rate, symbol, interest_rates)
        ir_cache.update(ir_cache_updated)


    print("Mejor tasa tomadora", ir_cache["lowest_ask_interest_rate"], '%', ir_cache["lair_ticker"], "Mejor tasa colocadora", ir_cache["highest_bid_interest_rate"], '%', ir_cache["hbir_ticker"] )
    mo.search_arbitrage_oportunity(ir_cache)
    print("Hr:", datetime.now().strftime('%H:%M:%S'))

def error_handler(message):
    print("Error Message Received: {0}".format(message))

def exception_handler(e):
    print("Exception Occurred: {0}".format(e.message))

# Conexión websocket
pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)

# Defino a que datos me voy a suscribir
entries = [pyRofex.MarketDataEntry.BIDS,
           pyRofex.MarketDataEntry.OFFERS,
           pyRofex.MarketDataEntry.LAST]

# Recibo datos del mercado
pyRofex.market_data_subscription(tickers=instruments,
                                 entries=entries)
