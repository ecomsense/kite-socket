from constants import logging


class Wsocket:
    def __init__(self, kite, sym_tkn):
        # self.instrument = ""
        self.ticks = {}
        self.kws = kite.kws()
        if isinstance(sym_tkn, list):
            self.sym_tkn = sym_tkn
        else:
            self.sym_tkn = [sym_tkn]
        print(self.sym_tkn)
        # Assign the callbacks.
        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self.kws.on_error = self.on_error
        self.kws.on_reconnect = self.on_reconnect
        self.kws.on_noreconnect = self.on_noreconnect

        # Infinite loop on the main thread. Nothing after this will run.
        # You have to use the pre-defined callbacks to manage subscriptions.
        self.kws.connect(threaded=True)

    def on_ticks(self, ws, ticks):
        # Callback to receive ticks.
        dct = {i["instrument_token"]: i["last_price"] for i in ticks}
        self.ticks = {**self.ticks, **dct}

    def on_connect(self, ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe(self.sym_tkn)
        # logging.info(f"on connect: {response}")
        ws.set_mode(ws.MODE_LTP, self.sym_tkn)

    def on_close(self, ws, code, reason):
        # On connection close stop the main loop
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    def on_error(self, ws, code, reason):
        # Callback when connection closed with error.
        logging.info(
            "Connection error: {code} - {reason}".format(code=code, reason=reason)
        )

    def on_reconnect(self, ws, attempts_count):
        # Callback when reconnect is on progress
        logging.info("Reconnecting: {}".format(attempts_count))

    # Callback when all reconnect failed (exhausted max retries)
    def on_noreconnect(self, ws):
        logging.info("Reconnect failed.")
