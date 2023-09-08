# Binance Bot

Este programa es un Bot para colocar Take Profit, Stop Loss y Trailing Stop de una posición que puede estar abierta o se puede definir. 

## Auto 
El programa principal es todo.py en el cual se definen las siguientes ordenes así:

### Orden Compra
Coloca la orden de compra o venta.

- client: Conexión con la API Binance
- simbolo: Criptomoneda que se quiere comprar
- tipo: Compra(BUY) o Venta(SELL)
- leverage: Apalancamiento (default 10)
- price_entry: Precio entrada
- porcentaje_usdt: Cantidad del todal de usdt colocar en la posición (default 1)

#### Resultado
Esta función devuelve:
orden_compra: Orden de compra 

### Orden Take Profit
Coloca la orden de Take Profit en donde se necesitan los siguientes párametros:

- client: Conexión con la API Binance
- orden: Posición activa en donde se quiere colocar el TP y SL
- ganancia: ROE(en porcentaje) de ganancia
- perdida: ROE(en porcentaje) de pérdida
- porcentaje_ts: ROE(en porcentaje) en donde se quiere activar el Trailing Stop

Además coloca la orden de __Stop Loss__ en donde se necesitan los siguientes párametros:

- client: Conexión con la API Binance
- orden: Posición activa en donde se quiere colocar el TP y SL
- perdida: ROE(en porcentaje) de pérdida

#### Resultado
Esta función devuelve:
- orden_sl: Orden del Stop Loss
- precio_act_tsl: Precio de activación de Trailing Stop
- lado: Compra(BUY) o Venta(SELL) 

### Orden Trailing Stop
Coloca la orden de Stop Loss y la va actualizando, necesitan los siguientes párametros:
- client: Conexión con la API Binance
- orden: Posición activa en donde se quiere colocar el TP y SL
- orden_sl: Orden del Stop Loss
- porcentaje_retorno: Desde que toca el precio de activación del Trailing Stop cuanto quiero que se devuelva (No se envia en porcentaje)

Para ejecutar el programa se debe activar el entorno virtual, crear un archivo de config.py donde se tenga el __apikey__ y __secret__, y llenar los parámetros de las lineas de compra o venta.

Si ya se tiene la posición activa se comentan las líneas de compra o venta y se pasa un diccionario con __orderId__ y __symbol__.

#### Resultado
El programa imprime 3 indicadores: la ganancia del Take Profit, la pérdida del Stop Loss y el Precio de Activación de Trailing Stop.

### Monitoreo 
El monitoreo es un programa para observar la posición activa con su Precio de Entrada, Precio Actual, Take Profit y Stop Loss.

#### Resultado 
El monitoreo imprime los siguientes indicadores de una posición abierta: 
- Criptomoneda
- Tipo de Compra: LONG O SHORT
- Precio de Entrada
- Precio Actual
- Take Profit
- Stop Loss