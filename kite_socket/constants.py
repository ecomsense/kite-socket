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
        logging.warning(f"using default {file} file")
    elif not flag and arg is None:
        logging.error(f"fill the {file} file and try again")
        __import__("sys").exit()

    return O_FUTL.get_lst_fm_yml(file)


O_CNFG = yml_to_obj()
O_SETG = yml_to_obj("settings.yml")
