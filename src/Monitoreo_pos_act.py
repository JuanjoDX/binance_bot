### Librerias 
from binance import Client
from datetime import datetime
import time
from binance.exceptions import BinanceAPIException

### API KEY y Cliente
apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
client = Client(apikey, secret)

### Monitoreo Constante
while True:

    ### Ver Operaciones Abiertas
    while True:
        try:
            res = client.futures_position_information()
            target_coin = {'symbol' : 'abc'}
            for position in res[::-1]:
                if float(position['positionAmt']) != 0:
                    target_coin = position
                    break
            break

        except BinanceAPIException as e:
            # Espera 0.5 segundos antes de intentar nuevamente
            time.sleep(0.5)


    ### Viendo Take Profit
    while True:
        try:
            res = client.futures_get_open_orders(symbol = target_coin["symbol"])
            pos_tp = {'symbol' : 'abc'}
            for position in res[::-1]:
                if (position['type']) == "LIMIT":
                    pos_tp = position
                    break
            break
        except BinanceAPIException as e:
            # Espera 0.5 segundos antes de intentar nuevamente
            time.sleep(0.5)


    ### Viendo Stop Lost
    while True:
        try:
            res = client.futures_get_open_orders(symbol = target_coin["symbol"])
            pos_sl = {'symbol' : 'abc'}
            for position in res[::-1]:
                if (position['type']) == "STOP_MARKET":
                    pos_sl = position
                    break
            break
        except BinanceAPIException as e:
            # Espera 0.5 segundos antes de intentar nuevamente
            time.sleep(0.5)
    
    ### Tipo de Compra
    aux = None
    if pos_tp["side"] == "SELL":
        aux = "LONG"
    else:
        aux = "SHORT"

    ### Color Fondo
    blue_background = "\033[44m"
    yellow_background = "\033[43m"
    reset_style = "\033[0m"

    while True:
        decimas = len(pos_tp["price"].split(".")[1])
        try:
            precio_entrada = str(round(float(client.futures_position_information(symbol = target_coin["symbol"])[0]['entryPrice']),decimas))
            break
        
        except BinanceAPIException as e:
            # Espera 0.5 segundos antes de intentar nuevamente
            time.sleep(0.5)

    ### Defiendo colores de fondo para el precio actual
    if aux == "SHORT":
        red_background = "\033[42m"
        green_background= "\033[41m"
    else:
        green_background = "\033[42m"
        red_background = "\033[41m"

    ### Monitoreo Continuo
    if target_coin["symbol"] == target_coin["symbol"]:
        print("Moneda:", target_coin["symbol"])
        print("Tipo:" , aux)
        
        print("Precio Entrada:" , f"{blue_background}{precio_entrada}{reset_style}")
        
        res = client.futures_symbol_ticker(symbol = target_coin["symbol"])
        fecha = datetime.fromtimestamp(res["time"]/1000).strftime("%d/%m/%Y %H:%M:%S")
        precio = res["price"]        

        if precio < precio_entrada:
            print("Precio Actual: ", f"{red_background}{precio}{reset_style}")
        else:
            print("Precio Actual: ", f"{green_background}{precio}{reset_style}")
        
        green_background = "\033[42m"
        red_background = "\033[41m"

        if pos_tp != None:
            print("Take Profit:   " ,f"{green_background}{pos_tp['price']}{reset_style}")
            print("Stop Lost:     " ,f"{red_background}{pos_sl['stopPrice']}{reset_style}")

        print(fecha)
        print("__________________________")
        time.sleep(10)
    else:
        print("EN ESPERA")
        
        aux = None
        if pos_tp["side"] == "SELL":
            aux = "LONG"
        else:
            aux = "SHORT"
        
        print("Moneda:", pos_tp["symbol"])
        print("Tipo:" , aux)

        res = client.futures_symbol_ticker(symbol = pos_tp["symbol"])
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        precio = pos_tp["price"]

        print("Precio Actual:  ", res["price"])
        print("Precio Entrada: ", precio)

        print(fecha)
        print("__________________________")
        time.sleep(5)