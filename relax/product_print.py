from relax.excel_common import (
    callback_product_name,
    callback_ticket_name,
    make_print_file_all,
    make_specail_ticket,
    make_ticket_special_print,
    move_to_print_folder,
)
from os import path as os_path, makedirs
from relax.util import global_config_data


def make_product_file(
    product_size_dict: dict,
    output_folder_path: str,
):
    target_path = os_path.join(output_folder_path, global_config_data["print"])
    if not os_path.isdir(target_path):
        makedirs(target_path)
        return
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
        move_to_print_folder(cover_source_path, target_path, "i")
        move_to_print_folder(product_source_path, target_path, "j")
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


def make_ticket_file(
    ticket_size_dict: dict,
    output_folder_path: str,
):
    target_path = os_path.join(output_folder_path, global_config_data["print"])
    if not os_path.isdir(target_path):
        makedirs(target_path)
        return

    ticket_source_path = os_path.join(
        output_folder_path, global_config_data["temp_ticket"]
    )
    if not ticket_source_path:
        return

    if not ticket_size_dict:
        move_to_print_folder(ticket_source_path, target_path, "k")
        return

    make_print_file_all(
        ticket_size_dict,
        ticket_source_path,
        target_path,
        "k",
        "pdf",
        callback_ticket_name,
    )

    make_specail_ticket(
        ticket_size_dict,
        ticket_source_path,
        "-",
        target_path,
        "k",
        "pdf",
        make_ticket_special_print,
    )
    pass
