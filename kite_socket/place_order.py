import requests
from constants import O_CNFG

api = O_CNFG["api"]
url = "https://kite.zerodha.com/connect/basket"
data = {
    "variety": "regular",
    "tradingsymbol": "INFY",
    "exchange": "NSE",
    "transaction_type": "BUY",
    "order_type": "MARKET",
    "quantity": 10,
    "readonly": False,
    "api_key": api,
}
r = requests.post(url, json=data)
if r is not None:
    print(r.text)
