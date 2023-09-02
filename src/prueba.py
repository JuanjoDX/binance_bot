### Librerias 
from binance import Client
import time
from binance.exceptions import BinanceAPIException

 ### API KEY y Cliente
apikey = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP'
secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
client = Client(apikey, secret)


while True:
        try:
            res = client.futures_position_information()
            target_coin = {'symbol' : 'abc'}
            for position in res[::-1]:
                if float(position['positionAmt']) != 0:
                    target_coin = position
                    break
            print(target_coin)
            break

        except BinanceAPIException as e:
            # Espera 0.5 segundos antes de intentar nuevamente
            time.sleep(0.5)


# while True:
#         try:
#             res = client.futures_get_open_orders(symbol = "1000SHIBUSDT")
#             pos_tp = {'symbol' : 'abc'}
#             for position in res[::-1]:
#                 if (position['type']) == "LIMIT":
#                     pos_tp = position
#                     break
#             print(pos_tp)
#             break
#         except BinanceAPIException as e:
#             print(e)
#             # Espera 0.5 segundos antes de intentar nuevamente
#             time.sleep(0.5)