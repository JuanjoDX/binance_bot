### Importar Programas
import Compra_automatica as ca
import TP_auto as tp
import Trailing_Stop as sl
from binance.exceptions import BinanceAPIException
from binance import Client
import time

### API KEY y Cliente
apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
client = Client(apikey, secret)

#orden = ca.compra_auto("1000SHIBUSDT","SELL",leverage = 50,price_entry=0.007880)
#orden = ca.compra_auto("1000SHIBUSDT","BUY",leverage = 50,price_entry=0.007824)

orden = {"orderId": "13651856025","symbol" : "1000SHIBUSDT"}
orden_sl, precio_act_tsl, lado = tp.tp_auto(client,orden,ganancia = 27,perdida = 50,porcentaje_ts = 0.6)
print("Precio activación Trailing Stop:",precio_act_tsl)

while True:
    try:
        precio_actual = float(client.futures_ticker(symbol = orden["symbol"])["lastPrice"])
    except BinanceAPIException as e:
        # Espera 0.2 segundos antes de intentar nuevamente
        time.sleep(0.2)

    if lado == "BUY":
        if precio_actual < float(precio_act_tsl):
            sl.sl_auto(client,orden,orden_sl,porcentaje_retorno = 10)
    else:
        if precio_actual > float(precio_act_tsl):
            sl.sl_auto(client,orden,orden_sl,porcentaje_retorno = 10)