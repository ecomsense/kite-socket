from constants import O_FUTL
import requests
import pandas as pd

diff = {"BANKNIFTY": 100, "NIFTY": 50}


class Symbols:
    def __init__(self, dump):
        self.dump = dump
        # download master records
        url = "https://api.kite.trade/instruments"
        if O_FUTL.is_file_not_2day(self.dump):
            print(f"dumping {url} to {self.dump}")
            r = requests.get(url)
            if r.status_code == 200:
                with open(self.dump, "w") as f:
                    f.write(r.text)

    def mk_opt_sym(self, symbol: str, expiry: str, strike: int, depth: int):
        """
        input:
            symbol : the first part of option
            expiry : str ex: 24507
            strike : strike price
            depth : number of strikes ex: 10 means 10 calls and 10 puts above
                and below atm total 22 strikes including atm strike
        ouput:
        """
        lst = []
        lst.append("NFO:" + symbol + expiry + str(strike) + "CE")
        lst.append("NFO:" + symbol + expiry + str(strike) + "PE")
        for v in range(1, depth):
            lst.append("NFO:" + symbol + expiry + str(strike + v * diff[symbol]) + "CE")
            lst.append("NFO:" + symbol + expiry + str(strike + v * diff[symbol]) + "PE")
            lst.append("NFO:" + symbol + expiry + str(strike - v * diff[symbol]) + "CE")
            lst.append("NFO:" + symbol + expiry + str(strike - v * diff[symbol]) + "PE")
        return lst

    def get_atm(self, diff, ltp) -> int:
        """
        input:
            diff: differance between strikes
            ltp: last traded price
        output:
            atm: atm strike price
        """
        current_strike = ltp - (ltp % diff)
        next_higher_strike = current_strike + diff
        if ltp - current_strike < next_higher_strike - ltp:
            return int(current_strike)
        return int(next_higher_strike)

    def get_tokens(self, lst):
        """
        input:
            lst: list of exchange and symbol seperated by ':'
        """
        self.dct = {}
        df = pd.read_csv(self.dump)
        for i in lst:
            lst_excsym = i.split(":")
            exch = lst_excsym[0]
            sym = lst_excsym[1]
            self.dct[i] = int(
                df.loc[(df["exchange"] == exch) & (df["tradingsymbol"] == sym)][
                    "instrument_token"
                ].values[0]
            )
        return self.dct
