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
#orden = ca.compra_auto(client, "1000SHIBUSDT","SELL", leverage = 50, price_entry=0.007750, porcentaje_usdt = 1)
orden = ca.compra_auto(client, "1000SHIBUSDT","BUY", leverage = 50, price_entry=0.007505, porcentaje_usdt = 1)

### Activar Programa dada la orderId
#orden = {"orderId": "13825171436","symbol" : "1000SHIBUSDT"}

orden_sl, precio_act_tsl, lado = tp.tp_auto(client,orden,ganancia = 10,perdida = 50,porcentaje_ts = 0.6)