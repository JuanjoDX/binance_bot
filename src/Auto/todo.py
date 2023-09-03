### Importar Programas
import Compra_automatica as ca
import TP_auto as tp
import Trailing_Stop as tsl
from binance.exceptions import BinanceAPIException
from binance import Client
import time
import config as cf

### Iniciar Cliente
client = Client(cf.apikey, cf.secret)

### Colocar Orden de Compra o Venta
#orden = ca.compra_auto(client, "1000SHIBUSDT","SELL", leverage = 50, price_entry=0.007880, porcentaje_usdt = 1)
#orden = ca.compra_auto(client, "1000SHIBUSDT","BUY", leverage = 50, price_entry=0.007824, porcentaje_usdt = 1)

### Activar Programa dada la orderId
# orden = {"orderId": "13657983712","symbol" : "1000SHIBUSDT"}

orden_sl, precio_act_tsl, lado = tp.tp_auto(client,orden,ganancia = 27,perdida = 50,porcentaje_ts = 0.001)
print("Precio activación Trailing Stop:",precio_act_tsl)

while True:
    try:
        precio_actual = float(client.futures_ticker(symbol = orden["symbol"])["lastPrice"])
    except BinanceAPIException as e:
        # Espera 0.2 segundos antes de intentar nuevamente
        time.sleep(0.2)

    if lado == "BUY":
        if precio_actual < float(precio_act_tsl):
            tsl.tsl_auto(client,orden,orden_sl,porcentaje_retorno = 10)
            break
    else:
        if precio_actual > float(precio_act_tsl):
            tsl.tsl_auto(client,orden,orden_sl,porcentaje_retorno = 10)
            break