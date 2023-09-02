### Importar Librerias
from binance import Client
from binance.exceptions import BinanceAPIException
import time

def sl_auto(client,orden,perdida):

    ### Posicion actual
    while True:
        try:
            pos_act = client.futures_position_information(symbol = orden["symbol"])[0]
            break
        except BinanceAPIException as e:
            # Espera 0.2 segundos antes de intentar nuevamente
            time.sleep(0.2)

    ### TP Limit Según lado
    roe = perdida

    aux = None
    decimas = len(orden["price"].split(".")[1])
    palanca = int(pos_act["leverage"])
    if orden["side"] == "SELL":
        aux = "BUY"
        precio_salida = str(round(float(pos_act["entryPrice"])*(1+(roe/(100*palanca))),decimas))
    else:
        aux = "SELL"
        precio_salida = str(round(float(pos_act["entryPrice"])*(1-(roe/(100*palanca))),decimas))

    ### Crear Orden SL
    orden_salida = client.futures_create_order(symbol = orden["symbol"],
                                side = aux,
                                stopPrice = precio_salida,
                                quantity = abs(int(pos_act["positionAmt"])),
                                type = 'STOP_MARKET',
                                timeinforce = 'GTC',
                                reduceOnly = True)

    ### Imprimir Perdida
    total_salida = float(orden_salida["stopPrice"])*float(orden_salida["origQty"])
    total_entrada = abs(float(pos_act["entryPrice"])*abs(int(pos_act["positionAmt"])))
    ganancia = total_salida - total_entrada
    comision = total_salida*0.0002 + total_entrada*0.0002 
    ganancia_neta = abs(ganancia-comision)
    print("La perdida es aproximandamente:", round(ganancia_neta,2))
    return(orden_salida)