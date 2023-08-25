### Importar Librerias
from binance import Client
import time
import SL_auto as sl

def tp_auto(orden):
    ### id de la orden
    orderid = orden["orderId"]
    simbolo = orden["symbol"]

    ### API KEY y Cliente
    apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
    secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
    client = Client(apikey, secret)

    ### Traer orden actualizada
    orden_act = client.futures_get_order(symbol = simbolo,
                                   orderId = orderid)

    c = 0
    while c <= 120:
        ### Traer estado Última Orden 
        status = orden_act["status"]

        if status == "FILLED":
            ### Posición Actual
            pos_act = client.futures_position_information(symbol = orden_act["symbol"])[0]

            ### TP Limit Según lado
            roe = 7

            aux = None
            decimas = len(orden_act["price"].split(".")[1])
            palanca = int(pos_act["leverage"])
            if orden_act["side"] == "SELL":
                aux = "BUY"
                precio_salida = str(round(float(pos_act["entryPrice"])*(1-(roe/(100*palanca))),decimas))
            else:
                aux = "SELL"
                precio_salida = str(round(float(pos_act["entryPrice"])*(1+(roe/(100*palanca))),decimas))

            ### Crear Orden TP
            orden_salida = client.futures_create_order(symbol = orden_act["symbol"],
                                        side = aux,
                                        price = precio_salida,
                                        quantity = abs(int(pos_act["positionAmt"])),
                                        type = 'LIMIT',
                                        timeinforce = 'GTC',
                                        reduceOnly = True)

            ### Imprimir Ganancia
            total_salida = float(orden_salida["price"])*float(orden_salida["origQty"])
            total_entrada = abs(float(pos_act["entryPrice"])*float(pos_act["positionAmt"]))
            ganancia = total_salida - total_entrada
            comision = total_salida*0.0002 + total_entrada*0.0002 
            ganancia_neta = abs(ganancia-comision)
            print("La ganancia es aproximandamente:", round(ganancia_neta,2))
            sl.sl_auto(orden_act)
            break
        elif c == 120:
            print("Se cancela la orden")
            client.futures_cancel_all_open_orders(symbol = orden_act["symbol"])
            break
        else:
            time.sleep(0.5)
            orden_act = client.futures_get_order(symbol = simbolo,
                                                 orderId = orderid)
            c = c+1
            print("Intento",c)