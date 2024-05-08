from constants import O_FUTL


def get_bypass(dct, sec_dir):
    try:
        from omspy_brokers.bypass import Bypass
    except ModuleNotFoundError:
        __import__("os").system(
            "pip install git+https://github.com/pannet1/omspy-brokers"
        )
        __import__("time").sleep(5)
        from omspy_brokers.bypass import Bypass
    try:
        tokpath = sec_dir + dct["userid"] + ".txt"
        enctoken = None
        if not O_FUTL.is_file_not_2day(tokpath):
            print(f"{tokpath} modified today ... reading {enctoken}")
            with open(tokpath, "r") as tf:
                enctoken = tf.read()
                if len(enctoken) < 5:
                    enctoken = None
        print(f"enctoken to broker {enctoken}")
        bypass = Bypass(dct["userid"], dct["password"], dct["totp"], tokpath, enctoken)
        if bypass.authenticate():
            if not enctoken:
                enctoken = bypass.kite.enctoken
                with open(tokpath, "w") as tw:
                    tw.write(enctoken)
    except Exception as e:
        print(f"unable to create bypass object  {e}")
    else:
        return bypass


def get_zerodha(fdct, sec_dir):
    try:
        from omspy_brokers.zerodha import Zerodha
    except ModuleNotFoundError:
        __import__("os").system(
            "pip install git+https://github.com/pannet1/omspy-brokers"
        )
        __import__("time").sleep(5)
        from omspy_brokers.zerodha import Zerodha
    try:
        zera = Zerodha(
            user_id=fdct["userid"],
            password=fdct["password"],
            totp=fdct["totp"],
            api_key=fdct["api_key"],
            secret=fdct["secret"],
            tokpath=sec_dir + fdct["userid"] + ".txt",
        )
        zera.authenticate()
    except Exception as e:
        print(f"exception while creating zerodha object {e}")
    finally:
        return zera


def remove_token(tokpath):
    __import__("os").remove(tokpath)
