try:
    from toolkit.logger import Logger
except ModuleNotFoundError:
    __import__("os").system(
        "pip install git+https://github.com/pannet1/toolkit")
    from toolkit.logger import Logger

    logging = Logger(10)

from toolkit.fileutils import Fileutils
from toolkit.kukoo import Kukoo

O_FUTL = Fileutils()
O_KUKO = Kukoo()
S_DATA = "data/"


def get_settings():
    # return the parent folder name
    folder = __import__("os").getcwd().split("/")[-1]
    # reverse the words seperated by -
    return "-".join(reversed(folder.split("-"))) + ".yml"


S_YAML = get_settings()
