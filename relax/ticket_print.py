from os import path as os_path, listdir, makedirs
from shutil import copyfile
from relax.file_common import (
    make_print_file_one,
    scale_pdf_size,
)
from relax.util import global_config_data, get_runtime
from time import time


def callback_ticket_name(zd, i, order_mark, page_size, postfix, zd_seq: int = 1):
    page_size_2 = f"-{page_size}" if page_size else ""
    zd_seq_2 = f"-{zd_seq}" if zd_seq else "-0"
    i_2 = f"-{i}" if i else "-0"
    return f"{zd}-{0}{order_mark}{zd_seq_2}{i_2}{page_size_2}.{postfix}"


def move_ticket_to_print_folder(
    source_path: str,
    target_path: str,
    order_mark: str,
    mapping_list: list,
    postfix: str,
    callback,
):
    def find_zd(mapping_list, file_name):
        for i, zd, zd_seq in mapping_list:
            if i == file_name:
                return (zd, zd_seq)
        return None

    file_list = listdir(source_path)
    for i in file_list:
        lst = i.rsplit(".", 1)
        if len(lst) != 2:
            continue
        if lst[1] != postfix:
            continue
        zd = find_zd(mapping_list, i)
        if not zd:
            continue
        unique_name = callback(zd[0], "", order_mark, "", postfix, zd[1])
        copyfile(
            os_path.join(source_path, i),
            os_path.join(target_path, unique_name),
        )
    pass


def get_ticket_zd_list(ticket_folder: str, sep: str) -> tuple[set, set]:
    file_list = listdir(ticket_folder)
    zd_set = set()
    zd_special_set = set()
    for i in file_list:
        if sep in i:
            zd = i.lstrip(sep, 1)[0]
            zd_special_set.add(zd)
            continue
        zd = i.lstrip(".", 1)[0]
        zd_set.add(zd)
    return zd_set, zd_special_set


def move_ticket_with_quantity(
    output_folder_path: str,
    ticket_folder_path: str,
    mapping_list: list[tuple],
    ticket_size_dict: dict,
):
    target_path = os_path.join(output_folder_path, global_config_data["print"])
    if not os_path.isdir(target_path):
        makedirs(target_path)
    order_mark = "h"
    postfix = "pdf"
    for i, zd, zd_seq in mapping_list:
        # if zd != "11034":
        #     continue
        zd_size_dict = ticket_size_dict[zd]
        make_print_file_one(
            zd,
            zd_size_dict["page_size"],
            zd_size_dict["page_quantity"],
            zd_size_dict["zd_class"],
            os_path.join(ticket_folder_path, i),
            target_path,
            order_mark,
            postfix,
            callback_ticket_name,
            zd_seq,
        )
        pass
    pass


def set_size_to_temp(
    ticket_folder_path: str,
    temp_ticket_path: str,
    temp_ticket_crop: str,
    mapping_list: list[tuple],
    ticket_size_dict: dict,
    margin_dict: dict,
    error_zd_list: list,
):
    for i, zd, _ in mapping_list:
        dict = ticket_size_dict[zd]
        page_size = dict["page_size"] if ticket_size_dict else "A4"
        page_orient: str = dict["page_orient"]
        # if zd != "11002":
        #     continue
        if not scale_pdf_size(
            ticket_folder_path,
            temp_ticket_path,
            temp_ticket_crop,
            i,
            margin_dict,
            page_size,
            page_orient,
        ):
            error_zd_list.append(zd)


def make_ticket_file(
    ticket_folder_path: str,
    output_folder_path: str,
    mapping_list: dict,
    ticket_size_dict: dict,
    ticket_data: dict,
):
    target_path = os_path.join(output_folder_path, global_config_data["print"])
    if not os_path.isdir(target_path):
        makedirs(target_path)

    temp_ticket_path = os_path.join(
        output_folder_path, global_config_data["temp_ticket"]
    )
    if not os_path.isdir(temp_ticket_path):
        makedirs(temp_ticket_path)
    temp_ticket_crop = os_path.join(
        temp_ticket_path, global_config_data["temp_ticket_crop"]
    )
    if not os_path.isdir(temp_ticket_crop):
        makedirs(temp_ticket_crop)

    error_zd_list = []
    t1 = time()
    margin_dict = ticket_data["margin"]
    set_size_to_temp(
        ticket_folder_path,
        temp_ticket_path,
        temp_ticket_crop,
        mapping_list,
        ticket_size_dict,
        margin_dict,
        error_zd_list,
    )
    t2 = time()
    if not ticket_size_dict:
        move_ticket_to_print_folder(
            temp_ticket_path,
            target_path,
            "k",
            mapping_list,
            "pdf",
            callback_ticket_name,
        )
    else:
        move_ticket_with_quantity(
            output_folder_path, temp_ticket_path, mapping_list, ticket_size_dict
        )
    t3 = time()
    print(get_runtime(t1, t2))
    print(get_runtime(t2, t3))
    return error_zd_list
    pass
