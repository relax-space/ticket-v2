import copy
from pandas import DataFrame, isnull as pd_isnull
from relax.excel_common import get_row_height_content, make_stamp, set_page_size
from relax.util import const_re, fill_zero_2, global_config_data
from datetime import datetime
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from os import makedirs, path as os_path


def _get_base_data(
    product_detail: dict, year: int, month: int, suppier: str, bill_date_str: str
) -> dict:
    row_content_0: str = (
        product_detail["row1"]["contents"][0]
        .replace(const_re["year"], str(year))
        .replace(const_re["month"], str(month))
    )

    row_content_3_0: str = product_detail["row3"]["contents"][0].replace(
        const_re["supplier"], suppier
    )

    bill_date = datetime.strptime(bill_date_str, "%Y-%m-%d")
    row_content_3_2: str = (
        product_detail["row3"]["contents"][2]
        .replace(const_re["year"], str(bill_date.year))
        .replace(const_re["month"], fill_zero_2(bill_date.month))
        .replace(const_re["day"], fill_zero_2(bill_date.day))
    )
    column_width_dict: dict = product_detail["column_width"]

    row_height_list = [
        product_detail["row1"]["height"],
        product_detail["row2"]["height"],
        product_detail["row3"]["height"],
        product_detail["row4"]["height"],
        product_detail["row_data"]["height"],
        product_detail["row_sum_1"]["height"],
        product_detail["row_sum_2"]["height"],
        product_detail["row_last"]["height"],
    ]
    row_content_list = [
        [row_content_0],
        product_detail["row2"]["contents"],
        [
            row_content_3_0,
            product_detail["row3"]["contents"][1],
            row_content_3_2,
        ],
        product_detail["row4"]["contents"],
        product_detail["row_data"]["contents"],
        product_detail["row_sum_1"]["contents"],
        product_detail["row_sum_2"]["contents"],
        product_detail["row_last"]["contents"],
    ]
    row_format_list = [
        product_detail["row1"]["formats"],
        product_detail["row2"]["formats"],
        product_detail["row3"]["formats"],
        product_detail["row4"]["formats"],
        product_detail["row_data"]["formats"],
        product_detail["row_sum_1"]["formats"],
        product_detail["row_sum_2"]["formats"],
        product_detail["row_last"]["formats"],
    ]
    setting_dict = {}
    setting_dict["column_width_dict"] = column_width_dict
    setting_dict["row_height_list"] = row_height_list
    setting_dict["row_content_list"] = row_content_list
    setting_dict["row_format_list"] = row_format_list
    setting_dict["product_name_settings"] = product_detail["product_name_settings"]
    return setting_dict

    pass


def set_row_format_list(
    wb1: Workbook,
    row_format_list: dict,
):
    wb_row_format_list = []
    for i in row_format_list:
        wb_row_format_list.append(wb1.add_format(i[0]))
    return wb_row_format_list


def write_content(
    df: DataFrame,
    wb1: Workbook,
    setting_dict: dict,
    zd_no: str,
    row_height_list_for_break: list,
):
    ws1: Worksheet = wb1.add_worksheet()
    ws1.center_horizontally()
    column_width_dict: dict = setting_dict["column_width_dict"]
    for k, v in column_width_dict.items():
        ws1.set_column(f"{k}:{k}", v)

    row_height_list: list = setting_dict["row_height_list"]
    for i, v in enumerate(row_height_list[:4]):
        ws1.set_row(i, v)
        row_height_list_for_break.append(v)
    row_content_list = setting_dict["row_content_list"]
    row_format_list = set_row_format_list(wb1, setting_dict["row_format_list"])
    row_index = 0
    ws1.merge_range(
        row_index,
        0,
        row_index,
        7,
        row_content_list[row_index][0],
        row_format_list[row_index],
    )
    bill_no = df.loc[0, "K"]
    row_index += 1
    ws1.merge_range(
        row_index,
        0,
        row_index,
        7,
        f"{row_content_list[row_index][0]}{bill_no}",
        row_format_list[row_index],
    )
    row_index += 1
    ws1.merge_range(
        row_index,
        0,
        row_index,
        3,
        f"{row_content_list[row_index][0]}",
        row_format_list[row_index],
    )
    ws1.merge_range(
        row_index,
        4,
        row_index,
        5,
        f"{row_content_list[row_index][1]}{zd_no}",
        row_format_list[row_index],
    )
    ws1.merge_range(
        row_index,
        6,
        row_index,
        7,
        f"{row_content_list[row_index][2]}",
        row_format_list[row_index],
    )
    row_index += 1
    titles: list = row_content_list[row_index][0].split(",")
    row_format_4 = row_format_list[row_index]
    for i, v in enumerate(titles):
        ws1.write(row_index, i, v, row_format_4)

    data_index = row_index
    data_index += 1
    row_format_data = row_format_list[data_index]
    row_height_data = row_height_list[data_index]
    data_index += 1
    row_format_sum_1 = row_format_list[data_index]
    row_content_sum_1 = row_content_list[data_index][0]
    row_height_sum_1 = row_height_list[data_index]
    data_index += 1
    row_format_sum_2 = row_format_list[data_index]
    row_content_sum_2 = row_content_list[data_index][0]
    row_height_sum_2 = row_height_list[data_index]
    data_index += 1
    row_format_last = row_format_list[data_index]
    row_content_last = row_content_list[data_index][0]
    row_height_last = row_height_list[data_index]

    data_len = len(df)
    receive_date_old = ""
    sum_old = 0
    seq_no = 1
    product_name_settings = setting_dict["product_name_settings"]
    max_china_count_per_row = product_name_settings["max_china_count_per_row"]
    height1 = product_name_settings["height1"]
    height2 = product_name_settings["height2"]
    height3 = product_name_settings["height3"]
    for i, row in df.iterrows():
        receive_date = row["B"]
        if receive_date_old and receive_date_old != receive_date:
            # 小计
            seq_no = 1
            row_index += 1
            ws1.set_row(row_index, row_height_sum_1)
            row_height_list_for_break.append(row_height_sum_1)
            ws1.merge_range(
                row_index, 0, row_index, 6, row_content_sum_1, row_format_sum_1
            )
            ws1.write(row_index, 7, sum_old, row_format_sum_1)
        sum_old = row["H"]

        row_index += 1
        row_height_data, product_name = get_row_height_content(
            row["E"], max_china_count_per_row, height1, height2, height3
        )
        ws1.set_row(row_index, row_height_data)
        row_height_list_for_break.append(row_height_data)
        ws1.write(row_index, 0, seq_no, row_format_data)
        ws1.write(row_index, 1, receive_date, row_format_data)
        ws1.write_string(row_index, 2, row["A"], row_format_data)
        ws1.write(row_index, 3, product_name, row_format_data)
        ws1.write(row_index, 4, row["G"], row_format_data)
        ws1.write(row_index, 5, row["F"], row_format_data)
        ws1.write(row_index, 6, row["I"], row_format_data)
        ws1.write(row_index, 7, row["J"], row_format_data)
        seq_no += 1

        receive_date_old = receive_date
        if i == data_len - 1:
            # 小计
            row_index += 1
            ws1.set_row(row_index, row_height_sum_1)
            row_height_list_for_break.append(row_height_sum_1)
            ws1.merge_range(
                row_index, 0, row_index, 6, row_content_sum_1, row_format_sum_1
            )
            ws1.write(row_index, 7, sum_old, row_format_sum_1)

            # 本账单合计
            row_index += 1
            ws1.set_row(row_index, row_height_sum_2)
            row_height_list_for_break.append(row_height_sum_2)
            ws1.merge_range(
                row_index, 0, row_index, 6, row_content_sum_2, row_format_sum_2
            )
            ws1.write(row_index, 7, row["M"], row_format_sum_2)
        pass
    row_index += 1
    ws1.set_row(row_index, row_height_last)
    row_height_list_for_break.append(row_height_last)
    ws1.write(row_index, 7, row_content_last, row_format_last)
    return ws1


def write_one_product(
    df: DataFrame,
    setting_dict: dict,
    zd_no: str,
    output_folder_path: str,
    product_input: dict,
    product_size_dict: dict,
    batch_size: dict,
    page_margin: dict,
):
    wb1 = Workbook(
        os_path.join(output_folder_path, f"{zd_no}.xlsx"),
        options={
            "strings_to_numbers": True,
            "constant_memory": True,
            "encoding": "utf-8",
        },
    )
    row_height_list: list = []
    ws1: Worksheet = write_content(df, wb1, setting_dict, zd_no, row_height_list)
    page_height = 768
    if product_size_dict:
        page_size = set_page_size(ws1, product_size_dict[zd_no])
        page_height = (
            batch_size["page_height_A4"]
            if page_size == "A4"
            else batch_size["page_height_A5"]
        )
    stamp = product_input["stamp"]
    if stamp["enable"]:
        stamp_product = stamp["product"]
        stamp["x_offset"] = stamp_product["x_offset"]
        stamp["y_offset"] = stamp_product["y_offset"]
        stamp["x_scale"] = stamp_product["x_scale"]
        stamp["y_scale"] = stamp_product["y_scale"]
        stamp["column"] = stamp_product["column"]
        make_stamp(ws1, row_height_list, page_height, stamp)
        ws1.set_margins(
            # left=1.78 / 2.5, right=1.78 / 2.5, top=1.91 / 2.5, bottom=0.5 / 2.5
            left=page_margin["left"] / 2.5,
            right=page_margin["right"] / 2.5,
            top=page_margin["top"] / 2.5,
            bottom=page_margin["bottom"] / 2.5,
        )
    ws1.set_footer("&C第&P页，共&N页")
    wb1.close()
    pass


def write_all_product(
    key_set: set,
    df_raw: DataFrame,
    year: int,
    month: int,
    suppier: str,
    bill_date_str: str,
    current_data: dict,
    output_folder_path,
    product_size_dict,
):
    output_folder_path = os_path.join(
        output_folder_path, global_config_data["temp_product"]
    )
    if not os_path.isdir(output_folder_path):
        makedirs(output_folder_path)
    product_input = copy.deepcopy(current_data["product"]["input"])
    batch_size = copy.deepcopy(current_data["batch_size"])
    product_detail = copy.deepcopy(current_data["product"]["output"]["product_detail"])
    setting_dict: dict = _get_base_data(
        product_detail, year, month, suppier, bill_date_str
    )
    page_margin = product_detail["page_margin"]
    for v in key_set:
        df = df_raw.loc[df_raw["C"] == v]
        df2 = df.sort_values(by=["B"])
        df2.reset_index(drop=True, inplace=True)
        write_one_product(
            df2,
            setting_dict,
            v,
            output_folder_path,
            product_input,
            product_size_dict,
            batch_size,
            page_margin,
        )
    pass
