### Importar Librerias
from binance import Client
from datetime import datetime
import time
from binance.exceptions import BinanceAPIException
import requests

def compra_auto(client, simbolo, tipo, price_entry, leverage = 10, porcentaje_usdt = 1):
    ### simbolo: moneda
    ### tipo: Compra(BUY) o Venta (SELL)
    ### leverage: apalancamiento
    ### price_entry: precio entrada
    ### porcentaje_usdt: cantidad del todal de usdt colocar en la posición
    
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
    total_usdt = (round(float(target["balance"]),2)*0.97)*porcentaje_usdt
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
    ### Imprime y devuelve la orden de compra
    print(orden_compra)
    return(orden_compra)