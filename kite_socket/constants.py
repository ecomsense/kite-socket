try:
    from toolkit.logger import Logger
except ModuleNotFoundError:
    __import__("os").system("pip install git+https://github.com/pannet1/toolkit")
    __import__("time").sleep(5)
    from toolkit.logger import Logger

from toolkit.fileutils import Fileutils

S_DATA = "../data/"
logging = Logger(10)
O_FUTL = Fileutils()


def yml_to_obj(arg=None):
    if not arg:
        # return the parent folder name
        folder = __import__("os").getcwd().split("/")[-1]
        # reverse the words seperated by -
        lst = folder.split("_")
        file = "-".join(reversed(lst))
        file = "../../" + file + ".yml"
    else:
        file = S_DATA + arg

    flag = O_FUTL.is_file_exists(file)

    if not flag and arg:
        logging.warning(f"using default {file=}")
    elif not flag and arg is None:
        logging.error(f"fill the {file=} file and try again")
        __import__("sys").exit()

    return O_FUTL.get_lst_fm_yml(file)


def win_yml_to_obj(arg=None):
    if not arg:
        file = "../../socket-kite.yml"
    else:
        file = S_DATA + arg

    flag = O_FUTL.is_file_exists(file)
    if not flag and arg:
        logging.warning(f"using default {file} file")
    elif not flag and arg is None:
        logging.error(f"fill the {file=} and try again")


def os_and_objects():
    try:
        if __import__("os").name != "nt":
            O_CNFG = yml_to_obj()
            O_SETG = yml_to_obj("settings.yml")
        else:
            O_CNFG = win_yml_to_obj()
            O_SETG = win_yml_to_obj("settings.yml")
    except Exception as e:
        logging.error(e)
        __import__("sys").exit()
    else:
        return O_CNFG, O_SETG


O_CNFG, O_SETG = os_and_objects()
