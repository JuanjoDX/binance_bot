### Importar Librerias
from binance import Client
from binance.exceptions import BinanceAPIException
import time 

def sl_auto(client,orden,orden_sl,porcentaje_retorno):
    
    roe = porcentaje_retorno
    orderid = orden["orderId"]
    simbolo = orden["symbol"]

    orderid_sl = orden_sl["orderId"]
    simbolo_sl = orden_sl["symbol"]

    ### Traer orden actualizada
    orden_act = client.futures_get_order(symbol = simbolo,
                                   orderId = orderid)
    
    orden_act_sl = client.futures_get_order(symbol = simbolo_sl,
                                   orderId = orderid_sl)

    ### Posicion actual
    while True:
        try:
            pos_act = client.futures_position_information(symbol = orden_act["symbol"])[0]
            break
        except BinanceAPIException as e:
            # Espera 0.2 segundos antes de intentar nuevamente
            print(e)
            time.sleep(0.2)
    

    ### TP Limit Según lado

    aux = None
    decimas = len(orden_act["price"].split(".")[1])
    palanca = int(pos_act["leverage"])

    while True:
        precio_salida_actual = float(orden_act_sl["stopPrice"])
        try:
            posicion = client.futures_position_information(symbol = orden_act["symbol"])
        except BinanceAPIException as e:
            # Espera 0.2 segundos antes de intentar nuevamente
            time.sleep(0.2)

        if len(posicion) > 0:
            try:
                precio_actual = client.futures_ticker(symbol = orden_act["symbol"])["lastPrice"]
            except BinanceAPIException as e:
                # Espera 0.2 segundos antes de intentar nuevamente
                time.sleep(0.2)

            if orden_act["side"] == "SELL":
                aux = "BUY"
                precio_salida = (round(float(precio_actual)*(1+(roe/(100*palanca))),decimas))
            else:
                aux = "SELL"
                precio_salida = (round(float(precio_actual)*(1-(roe/(100*palanca))),decimas))

            ### Crear Orden Trailing SL
            if orden_act["side"] == "SELL":
                if precio_salida_actual > precio_salida:
                    
                    client.futures_cancel_order(orderId = orderid_sl, symbol = simbolo_sl)
                    orden_salida = client.futures_create_order(symbol = orden_act["symbol"],
                                                            side = aux,
                                                            stopPrice = precio_salida,
                                                            quantity = abs(int(pos_act["positionAmt"])),
                                                            type = 'STOP_MARKET',
                                                            timeinforce = 'GTC',
                                                            reduceOnly = True)
                    
                    orden_act_sl = client.futures_get_order(symbol = orden_salida["symbol"],
                                    orderId = orden_salida["orderId"])

                    orderid_sl = orden_act_sl["orderId"]
                    simbolo_sl = orden_act_sl["symbol"]

            else:
                if precio_salida_actual < precio_salida:
                    
                    client.futures_cancel_order(orderId = orderid_sl, symbol = simbolo_sl)
                    orden_salida = client.futures_create_order(symbol = orden_act["symbol"],
                                                            side = aux,
                                                            stopPrice = precio_salida,
                                                            quantity = abs(int(pos_act["positionAmt"])),
                                                            type = 'STOP_MARKET',
                                                            timeinforce = 'GTC',
                                                            reduceOnly = True)
                    
                    orden_act_sl = client.futures_get_order(symbol = orden_salida["symbol"],
                                    orderId = orden_salida["orderId"])

                    orderid_sl = orden_act_sl["orderId"]
                    simbolo_sl = orden_act_sl["symbol"]

            print("Reevaluando")
            try:
                posicion = client.futures_position_information(symbol = orden_act["symbol"])
            except BinanceAPIException as e:
                # Espera 0.2 segundos antes de intentar nuevamente
                time.sleep(0.2)
            time.sleep(1)