### Importar Librerias
from binance import Client
from datetime import datetime
import time
from binance.exceptions import BinanceAPIException
import math

def compra_auto(simbolo, tipo, price_entry, leverage = 10):
    ### simbolo: moneda
    ### tipo: Compra(BUY) o Venta (SELL)
    ### leverage: apalancamiento
    ### price_entry: precio entrada

    ### API KEY y Cliente
    apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
    secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
    client = Client(apikey, secret)

    client.futures_cancel_all_open_orders(symbol = simbolo)
    
    ### Traer Balance USDT de la cuenta
    while True:
        try:
            res = client.futures_account_balance()
            asset = "USDT"

            target = None
            for position in res:
                if position['asset'] == asset:
                    target = position
                    break
            break
        except BinanceAPIException as e:
            # Espera 0.2 segundos antes de intentar nuevamente
            time.sleep(0.2)

    ### Orden Operación
    total_usdt = round(float(target["balance"]),2) - 0.01
    cantidad_monedas = round((total_usdt*leverage/price_entry)//1)

    ### Modificar palanca 
    client.futures_change_leverage(symbol=simbolo, leverage=leverage)

    ### Mandar Orden
    orden_compra = client.futures_create_order(symbol = simbolo,
                                side = tipo,
                                price = str(price_entry),
                                quantity = cantidad_monedas,
                                type = 'LIMIT',
                                timeinforce = 'GTC')
    print(orden_compra)
    return(orden_compra)