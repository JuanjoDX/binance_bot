### Importar Programas
import Compra_automatica as ca
import TP_auto as tp

#orden = ca.compra_auto("1000SHIBUSDT","SELL",leverage = 10,price_entry=0.008465)
orden = ca.compra_auto("1000SHIBUSDT","BUY",leverage = 10,price_entry=0.008540)


#orden = {"orderId": "13406046531","symbol" : "1000SHIBUSDT"}
tp.tp_auto(orden)