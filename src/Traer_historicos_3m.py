
### Importar Librerias 
from binance import Client
import pandas as pd
from datetime import datetime, timedelta

### API KEYS y Cliente
apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
client = Client(apikey, secret)

### Hora Servidor y hora inicio
res = client.get_exchange_info()
hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')
hora_inicio = hora_ser-timedelta(minutes = 500)

### Temporalidad
t = "3m"

### Simbolo
simbolo = "1000SHIBUSDT"

### Funcion historico 
def historico(sym, t, inicio, fin):
    historical = client.futures_historical_klines(symbol=sym,
                                                  interval=t,
                                                  start_str=str(inicio),
                                                  end_str=str(fin))

    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                        'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']

    hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
    hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)
    
    hist_df["Open Time"] = hist_df["Open Time"] - timedelta(hours = 5)
    hist_df["Close Time"] = hist_df["Close Time"] - timedelta(hours = 5)
    hist_df.to_csv("C:/Users/Usuario/Proyectos/Bot Trading/data/data_shibusdt_" + t + ".csv",index = False)

historico(simbolo, t, hora_inicio, hora_ser)