from binance.client import Client
symbol='XRPUSDT'

api_key='o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
api_secret='OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'

client = Client(api_key=api_key, api_secret=api_secret,testnet = False)


#stop loss order
buyorder=client.futures_create_order(symbol=symbol,side='BUY',type='STOP_MARKET',stopPrice='0.41',closePosition='true') 

#take profit order
sellorder=client.futures_create_order(symbol=symbol,side='SELL',type='TAKE_PROFIT_MARKET',stopPrice='0.45',closePosition='true')   

