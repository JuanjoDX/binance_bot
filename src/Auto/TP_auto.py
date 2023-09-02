### Importar Librerias
from binance import Client
from binance.exceptions import BinanceAPIException
import time 
import SL_auto as sl

def tp_auto(client,orden,ganancia,perdida,porcentaje_ts):
    ### id de la orden
    orderid = orden["orderId"]
    simbolo = orden["symbol"]

    ### Traer orden actualizada
    orden_act = client.futures_get_order(symbol = simbolo,
                                   orderId = orderid)

    c = 0
    while c <= 120:
        ### Traer estado Última Orden 
        status = orden_act["status"]

        if status == "FILLED":
            ### Posición Actual
            while True:
                try:
                    pos_act = client.futures_position_information(symbol = orden["symbol"])[0]
                    break
                except BinanceAPIException as e:
                    # Espera 0.2 segundos antes de intentar nuevamente
                    time.sleep(0.2)

            ### TP Limit Según lado
            roe = ganancia

            aux = None
            decimas = len(orden_act["price"].split(".")[1])
            palanca = int(pos_act["leverage"])
            if orden_act["side"] == "SELL":
                aux = "BUY"
                precio_salida = str(round(float(pos_act["entryPrice"])*(1-(roe/(100*palanca))),decimas))
                precio_act_tsl = str(round(float(pos_act["entryPrice"])*(1-(roe*porcentaje_ts/(100*palanca))),decimas))
            else:
                aux = "SELL"
                precio_salida = str(round(float(pos_act["entryPrice"])*(1+(roe/(100*palanca))),decimas))
                precio_act_tsl = str(round(float(pos_act["entryPrice"])*(1+(roe*porcentaje_ts/(100*palanca))),decimas))                

            ### Crear Orden TP
            while True:
                try:
                    orden_salida = client.futures_create_order(symbol = orden_act["symbol"],
                                        side = aux,
                                        price = precio_salida,
                                        quantity = abs(int(pos_act["positionAmt"])),
                                        type = 'LIMIT',
                                        timeinforce = 'GTC',
                                        reduceOnly = True)
                    break
                except BinanceAPIException as e:
                    # Espera 0.2 segundos antes de intentar nuevamente
                    time.sleep(0.2)

            ### Imprimir Ganancia
            total_salida = float(orden_salida["price"])*float(orden_salida["origQty"])
            total_entrada = abs(float(pos_act["entryPrice"])*float(pos_act["positionAmt"]))
            ganancia = total_salida - total_entrada
            comision = total_salida*0.0002 + total_entrada*0.0002 
            ganancia_neta = abs(ganancia-comision)
            print("La ganancia es aproximandamente:", round(ganancia_neta,2))
            return(sl.sl_auto(client,orden_act,perdida),precio_act_tsl,aux)
        
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