from constants import logging, O_CNFG, O_SETG, S_DATA
from login import get_bypass
from symbols import Symbols, diff
from wsocket import Wsocket
from traceback import print_exc
from typing import Dict, List


def mk_lst_to_subscribe(O_SYM, O_API) -> List:
    try:
        k = "BANKNIFTY"
        ltp = 48048
        atm = O_SYM.get_atm(diff[k], ltp=ltp)
        logging.info(f"atm {atm}")

        EXTKN: List = O_SYM.mk_opt_sym(
            symbol=k,
            expiry=O_SETG[k]["expiry"],
            strike=atm,
            depth=O_SETG[k]["depth"],
        )
        EXTKN.append(O_SETG[k]["spot"])
        EXTKN.append(O_SETG[k]["future"])
    except Exception as e:
        logging.error(e)
        print_exc()
    else:
        return EXTKN


def init():
    O_API = get_bypass(O_CNFG["bypass"], S_DATA)
    # orders
    print(O_API.orders)

    # prepare for websocket
    O_SYM = Symbols(S_DATA + "instruments.csv")
    exchsym: List = mk_lst_to_subscribe(O_SYM, O_API)
    sym_tkn: Dict = O_SYM.get_tokens(exchsym)
    ws = Wsocket(O_API.kite, list(sym_tkn.values()))
    while True:
        if ws.kws.is_connected():
            quotes = {k: ws.ticks[v] for k, v in sym_tkn.items()}
            print(quotes)
        __import__("time").sleep(1)


init()
