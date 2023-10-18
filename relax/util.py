import json

_raw_data = []
_config_data = {}
const_re = {
    "year": "@@@@",
    "month": "####",
    "day": "$$$$",
    "supplier": "||||",
}


def init_raw_data() -> list:
    with open("config/data.json", mode="r", encoding="utf8") as f:
        d = json.load(f)
    _raw_data.extend(d)
    return d


def update_raw_data():
    with open("config/data.json", mode="w", encoding="utf8") as f:
        json.dump(_raw_data, f, ensure_ascii=False)


def get_current_data(menu_name: str) -> dict:
    for i in _raw_data:
        if i["menu_name"] == menu_name:
            return i
    return None


def delete_current_data(menu_name: str):
    index = -1
    for i, v in enumerate(_raw_data):
        if v["menu_name"] == menu_name:
            index = i
            break
    del _raw_data[index]


def update_current_data(old_name, new_name: str) -> dict:
    for i in _raw_data:
        if i["menu_name"] == old_name:
            i["menu_name"] = new_name
            return i
    return None


def get_template_data() -> dict:
    with open("config/template.json", mode="r", encoding="utf8") as f:
        return json.load(f)


def init_const() -> dict:
    with open("config/var_config.json", mode="r", encoding="utf8") as f:
        data = json.load(f)
        _config_data.update(data)


def fill_zero_2(i: int) -> str:
    return f"{i:0>2}"
