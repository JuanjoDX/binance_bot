### Funcion historico 
def historico(client, sym, inicio, fin, t = "1m"):
    import pandas as pd
    from datetime import datetime, timedelta

    ### Se trae el historico del simbolo seleccionado en la temporalidad, con fechas de inicio y fin
    historical = client.futures_historical_klines(symbol=sym,
                                                  interval=t,
                                                  start_str=str(inicio),
                                                  end_str=str(fin))

    hist_df = pd.DataFrame(historical)
    hist_df.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 
                        'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore']

    hist_df['Open Time'] = pd.to_datetime(hist_df['Open Time']/1000, unit='s')
    hist_df['Close Time'] = pd.to_datetime(hist_df['Close Time']/1000, unit='s')

    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']
    hist_df[numeric_columns] = hist_df[numeric_columns].apply(pd.to_numeric, axis=1)
    
    ### Se restan 5 horas para adaptarlo a la hora regional
    hist_df["Open Time"] = hist_df["Open Time"] - timedelta(hours = 5)
    hist_df["Close Time"] = hist_df["Close Time"] - timedelta(hours = 5)

    return(hist_df)