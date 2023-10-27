from json import load as json_load, dump as json_dump
from os import path as os_path
from time import strftime, gmtime

global_raw_data = []
global_config_data = {}
const_re = {
    "year": "@@@@",
    "month": "####",
    "day": "$$$$",
    "supplier": "||||",
}

global_widgets = {}
global_dict_chk_var = {
    "_import_var": "",
    "_page_size_var": "",
    "_stamp_var": "",
    "_import_var_option": "",
}


def init_raw_data() -> list:
    with open("config/data.json", mode="r", encoding="utf8") as f:
        d = json_load(f)
    global_raw_data.extend(d)
    return d


def update_raw_data():
    with open("config/data.json", mode="w", encoding="utf8") as f:
        json_dump(global_raw_data, f, ensure_ascii=False)


def get_current_data(menu_name: str) -> dict:
    for i in global_raw_data:
        if i["menu_name"] == menu_name:
            return i
    return None


def delete_current_data(menu_name: str):
    index = -1
    for i, v in enumerate(global_raw_data):
        if v["menu_name"] == menu_name:
            index = i
            break
    del global_raw_data[index]


def update_current_data(old_name, new_name: str) -> dict:
    for i in global_raw_data:
        if i["menu_name"] == old_name:
            i["menu_name"] = new_name
            return i
    return None


def get_template_data() -> dict:
    with open("config/template.json", mode="r", encoding="utf8") as f:
        return json_load(f)


def init_const() -> dict:
    with open("config/var_config.json", mode="r", encoding="utf8") as f:
        data = json_load(f)
        global_config_data.update(data)


def fill_zero_2(i: int) -> str:
    return f"{i:0>2}"


def get_unique_name(base_path: str, name: str, postfix: str, seq_no: int = 0) -> str:
    unique_name = f"{name}-{seq_no}" if seq_no else name
    if not os_path.isfile(os_path.join(base_path, f"{unique_name}{postfix}")):
        return f"{unique_name}{postfix}"
    seq_no += 1
    return get_unique_name(base_path, name, postfix, seq_no)


def mm_to_pixel(mm: float):
    # Notes how to calculate it:
    # 1. Get the size of the paper in mm
    # 2. Convert it to inches (25.4 millimeters are equal to 1 inches)
    # 3. Convert it to pixels ad 72dpi (1 inch is equal to 72 pixels)
    return int((72 / 25.4) * mm)


def get_runtime(start_stamp, end_stamp):
    return strftime("%H小时%M分%S秒", gmtime(end_stamp - start_stamp))
