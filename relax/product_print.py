from shutil import copyfile
from relax.file_common import (
    make_print_file_one,
)
from os import path as os_path, makedirs, listdir
from relax.util import global_config_data


def callback_product_name(zd, i, order_mark, page_size, postfix, zd_seq: int = 1):
    page_size_2 = f"-{page_size}" if page_size else f""
    return f"{zd}-{i}{order_mark}{page_size_2}.{postfix}"


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
        source_file_path = os_path.join(source_path, f"{zd}.{postfix}")
        make_print_file_one(
            zd,
            page_size,
            page_quantity,
            source_file_path,
            target_path,
            order_mark,
            postfix,
            callback,
        )
    pass


def move_product_to_print_folder(source_path: str, target_path: str, order_mark: str):
    file_list = listdir(source_path)
    for i in file_list:
        lst = i.rsplit(".", 1)
        if len(lst) != 2:
            continue
        target_name = callback_product_name(lst[0], 1, order_mark, "", "xlsx")
        copyfile(
            os_path.join(source_path, i),
            os_path.join(target_path, target_name),
        )
    pass


def make_product_file(
    product_size_dict: dict,
    output_folder_path: str,
):
    target_path = os_path.join(output_folder_path, global_config_data["print"])
    if not os_path.isdir(target_path):
        makedirs(target_path)
    cover_source_path = os_path.join(
        output_folder_path, global_config_data["temp_cover"]
    )
    if not cover_source_path:
        return
    product_source_path = os_path.join(
        output_folder_path, global_config_data["temp_product"]
    )
    if not product_source_path:
        return

    if not product_size_dict:
        move_product_to_print_folder(cover_source_path, target_path, "i")
        move_product_to_print_folder(product_source_path, target_path, "j")
        return

    make_print_file_all(
        product_size_dict,
        cover_source_path,
        target_path,
        "i",
        "xlsx",
        callback_product_name,
    )
    make_print_file_all(
        product_size_dict,
        product_source_path,
        target_path,
        "j",
        "xlsx",
        callback_product_name,
    )

    pass
