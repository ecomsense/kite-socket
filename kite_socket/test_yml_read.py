from constants import O_FUTL

raw_file = O_FUTL.read_file("../settings.yml")
print(raw_file)
obj = O_FUTL.get_lst_fm_yml("../settings.yml")
print(obj)
