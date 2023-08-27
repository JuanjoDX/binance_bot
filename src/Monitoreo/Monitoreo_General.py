### Importar Librerias 
from binance import Client
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from Traer_historicos import historico
from Indicadores import indicadores

inicio = datetime.now()
### API KEYS y Cliente
apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
client = Client(apikey, secret)

### Hora Servidor y hora inicio
res = client.get_exchange_info()
hora_ser = pd.to_datetime(res["serverTime"]/1000, unit='s')

### Cambiar los minutos de cuanto tiempo atras se requiere
hora_inicio = hora_ser-timedelta(minutes = 500) 

### Temporalidad
temporalidad = "1m"

### Simbolo
simbolo = "1000SHIBUSDT"

### Traer historico requerido
df = historico(client,sym = simbolo, 
               inicio = hora_inicio, fin = hora_ser, t = temporalidad)

### Quitar Información No Necesaria
df.drop(["Volume","Quote Asset Volume","Number of Trades","TB Base Volume", "TB Quote Volume","Ignore"], axis = 1, inplace = True)

### Añadir indicadores
df = indicadores(df,t = temporalidad)

print(df.tail(10))
fin = datetime.now()
print(fin-inicio)