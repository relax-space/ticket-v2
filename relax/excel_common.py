from os import path as os_path, listdir, rename
from shutil import copyfile
from pandas import read_excel
from math import floor
from xlsxwriter.worksheet import Worksheet

from relax.util import loop_name


def get_page_size_list(batch_size: dict) -> tuple[dict, dict]:
    is_page_size: bool = batch_size["enable"]
    use_column_str: str = batch_size["column_name"]
    size_path: str = batch_size["path"]
    if not is_page_size:
        return {}, {}
    usecols = use_column_str.split(",")
    df = read_excel(size_path, usecols=usecols)
    # 客户id,筹措清单打印大小,筹措清单份数,发票打印大小,发票份数
    df.columns = ["A", "B", "C", "D", "E"]
    zd_set = set()
    product_size_dict = {}
    ticket_size_dict = {}
    df.dropna(subset=["C", "E"], inplace=True)
    for _, v in df.iterrows():
        zd = v["A"]
        p1_size = v["B"]
        p1_quantity = int(v["C"])
        p2_size = v["D"]
        p2_quantity = int(v["E"])
        for i in [p1_size, p2_size]:
            if i not in ["A4", "A5"]:
                continue
        product_size_dict[zd] = {
            "zd": zd,
            "page_size": p1_size,
            "page_quantity": p1_quantity,
        }
        ticket_size_dict[zd] = {
            "zd": zd,
            "page_size": p2_size,
            "page_quantity": p2_quantity,
        }
        zd_set.add(zd)
        pass
    return zd_set, product_size_dict, ticket_size_dict
    pass


def get_row_height_byrow(
    row_count: int,
    height1: int = 15,
    height2: int = 7,
    height3: int = 11,
) -> int:
    total_height = 0
    match row_count:
        case 0 | 1:
            total_height = height1
        case 2:
            total_height = height1 + height2
        case _:
            total_height = height1 + height2 + (row_count - 2) * height3
    return total_height


def get_row_count(raw: str, max_china_per_row: int = 17) -> tuple[int, str]:
    row_count = 1
    total_count = len(raw.encode("utf8"))
    char_count_per_row = max_china_per_row * 3
    if total_count <= char_count_per_row:
        """
        处理大多数数据
        """
        return row_count, raw
    else:
        break_list = []
        char_list = list(raw)
        i = 0
        current_char_count = 0
        char_count = len(char_list)
        while i < char_count:
            v = len(char_list[i].encode("utf8"))
            current_char_count += v
            if current_char_count > char_count_per_row * row_count:
                current_char_count -= v
                i -= 1
                break_list.append(i)
                row_count += 1
            i += 1

        new_content = ""
        break_list_count = len(break_list)
        for i, v in enumerate(break_list):
            if i == 0:
                new_content += raw[0 : v + 1] + "\n"
            else:
                pre = break_list[i - 1]
                new_content += raw[pre + 1 : v + 1] + "\n"
            if i == break_list_count - 1:
                new_content += raw[v + 1 :]
        return row_count, new_content


def get_row_height_content(
    raw: str,
    byte_per_row: int = 17,
    height1: int = 15,
    height2: int = 7,
    height3: int = 11,
):
    row_count, new_content = get_row_count(raw, byte_per_row)
    row_height = get_row_height_byrow(row_count, height1, height2, height3)
    return row_height, new_content


def set_page_size(ws1: Worksheet, size_dict: dict):
    page_size = size_dict["page_size"]
    page_size_index = 9
    if page_size == "A4":
        ws1.set_portrait()
    elif page_size == "A5":
        ws1.set_landscape()
        page_size_index = 11
    ws1.set_paper(page_size_index)
    return page_size


def make_stamp(ws1: Worksheet, row_height_list: list, page_height: int, stamp: dict):
    column = stamp["column"]
    img_path = stamp["path"]
    x_scale = stamp["x_scale"]
    y_scale = stamp["y_scale"]
    x_offset = stamp["x_offset"]
    y_offset = stamp["y_offset"]
    page_count = 1
    total_height = 0
    break_list = []
    current_height = 0
    for height in row_height_list:
        total_height += height

    i = 0
    row_count = len(row_height_list)
    while i < row_count:
        v = row_height_list[i]
        current_height += v
        if current_height > page_height * page_count:
            current_height -= v
            i -= 1
            break_list.append(i)
            page_count += 1
        i += 1

    # 保证最后一页，至少有两行数据
    rest_height = total_height - current_height
    if rest_height == row_height_list[-1]:
        if break_list:
            break_list.pop()
        break_list.append(row_count - 2)

    dic_img = {
        "x_scale": x_scale,
        "y_scale": y_scale,
        "x_offset": x_offset,
        "y_offset": y_offset,
    }

    img_row_index = 2
    if break_list:
        img_row_index = break_list[-1] + 1

    ws1.insert_image(
        f"{column}{img_row_index}",
        img_path,
        dic_img,
    )
    ws1.set_h_pagebreaks(break_list)
    pass


def callback_product_name(target_path, zd, i, order_mark, page_size, postfix):
    return f"{zd}-{i}{order_mark}-{page_size}.{postfix}"


def callback_ticket_name(target_path, zd, i, order_mark, page_size, postfix):
    return f"{zd}-{0}{order_mark}{i}-{page_size}.{postfix}"


def make_ticket_special_print(target_path, zd, i, order_mark, page_size, postfix):
    pre = f"{zd}-0{order_mark}{i}"
    post = f"-{page_size}.{postfix}"
    return loop_name(target_path, pre, post, i)


def make_specail_ticket(
    ticket_size_dict: dict,
    source_path: str,
    sep: str,
    target_path: str,
    order_mark: str,
    postfix: str,
    callback: str,
):
    file_list = listdir(source_path)
    specail_list: list[str] = []
    for i in file_list:
        if sep not in i:
            continue
        specail_list.append(i)

    for i in specail_list:
        lst = i.lstrip(sep, 1)
        zd = lst[0]
        one_size = ticket_size_dict[zd]
        make_print_file_one(
            zd,
            one_size["page_size"],
            one_size["page_quantity"],
            source_path,
            target_path,
            order_mark,
            postfix,
            callback,
        )
    pass


def make_print_file_one(
    zd: str,
    page_size: str,
    page_quantity: int,
    source_path: str,
    target_path: str,
    order_mark: str,
    postfix: str,
    callback,
):
    source_file_path = os_path.join(source_path, f"{zd}.{postfix}")
    if not os_path.isfile(source_file_path):
        return
    for i in range(page_quantity):
        target_name = callback(target_path, zd, i, order_mark, page_size, postfix)
        copyfile(source_file_path, os_path.join(target_path, target_name))


def move_to_print_folder(source_path: str, target_path: str, order_mark: str):
    file_list = listdir(source_path)
    for i in file_list:
        lst = i.rsplit(".", 1)
        if len(lst) != 2:
            continue
        rename(
            os_path.join(source_path, i),
            os_path.join(target_path, f"{lst[0]}{order_mark}{lst[1]}"),
        )
    pass


def make_print_file_all(
    size_dict: dict,
    source_path: str,
    target_path: str,
    order_mark: str,
    postfix: str,
    callback,
):
    for v in size_dict.values():
        zd = v["zd"]
        page_size = v["page_size"]
        page_quantity = v["page_quantity"]
        make_print_file_one(
            zd,
            page_size,
            page_quantity,
            source_path,
            target_path,
            order_mark,
            postfix,
            callback,
        )
    pass