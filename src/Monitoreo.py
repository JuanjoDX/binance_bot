### Librerias 
from binance import Client
from datetime import datetime
import time
from binance.exceptions import BinanceAPIException

### Monitoreo Constante
while True:

    ### API KEY y Cliente
    apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
    secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
    client = Client(apikey, secret)

    ### Viendo Precio Entrada
    res = client.futures_get_all_orders()
    status = "FILLED"

    target_status = None
    for position in res[::-1]:
        if position['status'] == status:
            target_status = position
            break

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
            # Espera 5 segundos antes de intentar nuevamente
            time.sleep(5)

    ### Viendo TakeProfit
    res2 = client.futures_get_all_orders()
    status = "NEW"

    target_status2 = None
    for position in res2[::-1]:
        if position['status'] == status:
            target_status2 = position
            break

    ### Tipo de Compra
    aux = None
    if target_status["side"] == "SELL":
        aux = "SHORT"
    else:
        aux = "LONG"

    ### Color Fondo
    blue_background = "\033[44m"
    green_background = "\033[42m"
    red_background = "\033[41m"
    yellow_background = "\033[43m"
    reset_style = "\033[0m"

    while True:
        try:
            precio_entrada = client.futures_position_information(symbol = target_status["symbol"])[0]['entryPrice']
            break
        
        except BinanceAPIException as e:
            # Espera 5 segundos antes de intentar nuevamente
            time.sleep(5)

    if aux == "SHORT":
        red_background = "\033[42m"
        green_background= "\033[41m"

    ### Monitoreo Continuo
    if target_coin["symbol"] == target_status["symbol"]:
        print("Moneda:", target_status["symbol"])
        print("Tipo:" , aux)
        
        print("Precio Entrada:" , f"{blue_background}{precio_entrada}{reset_style}")
        
        res = client.futures_symbol_ticker(symbol = target_status["symbol"])
        fecha = datetime.fromtimestamp(res["time"]/1000).strftime("%d/%m/%Y %H:%M:%S")
        precio = res["price"]

        if precio < precio_entrada:
            print("Precio Actual: ", f"{red_background}{precio}{reset_style}")
        else:
            print("Precio Actual: ", f"{green_background}{precio}{reset_style}")
        
        if target_status2 != None:
            print("Take Profit:   " ,f"{yellow_background}{target_status2['price']}{reset_style}")
        print(fecha)
        print("__________________________")
        time.sleep(10)
    else:
        print("EN ESPERA")
        
        aux = None
        if target_status2["side"] == "SELL":
            aux = "SHORT"
        else:
            aux = "LONG"
        
        print("Moneda:", target_status2["symbol"])
        print("Tipo:" , aux)

        res = client.futures_symbol_ticker(symbol = target_status2["symbol"])
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        precio = target_status2["price"]

        print("Precio Actual:  ", res["price"])
        print("Precio Entrada: ", precio)

        print(fecha)
        print("__________________________")
        time.sleep(5)