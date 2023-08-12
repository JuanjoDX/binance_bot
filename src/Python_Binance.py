import time 
from binance.cm_futures import CMFutures
from datetime import datetime
client = CMFutures(
    key = 'o4xp0nX8Nr3RsQIAQDBs7ZZivwpoLHPZsDQU48dmWX8heBKpSgPOS0M9NZwHHbEP',
    secret = 'OwjJSwLt0szX7qq62Xqd7evsc345eCLCTrYIVTdIND4HORYJ4DDz7lmGnDGCMiwq'
)
res = client.funding_rat()

print(res)