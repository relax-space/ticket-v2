import copy
from pandas import DataFrame
from relax.file_common import make_stamp, set_page_size
from relax.util import const_re, global_config_data
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from os import makedirs, path as os_path


def _get_base_data(cover: dict, year: int, month: int, suppier: str) -> dict:
    row_content_1: str = (
        cover["row1"]["contents"][0]
        .replace(const_re["year"], str(year))
        .replace(const_re["month"], str(month))
    )

    row_content_2: str = cover["row2"]["contents"][0].replace(
        const_re["supplier"], suppier
    )
    column_width_dict: dict = cover["column_width"]

    row_height_list = [
        cover["row1"]["height"],
        cover["row2"]["height"],
        cover["row3"]["height"],
        cover["row_data"]["height"],
        cover["row_last"]["height"],
    ]
    row_content_list = [
        [row_content_1],
        [row_content_2],
        cover["row3"]["contents"],
        cover["row_data"]["contents"],
        cover["row_last"]["contents"],
    ]
    row_format_list = [
        cover["row1"]["formats"],
        cover["row2"]["formats"],
        cover["row3"]["formats"],
        cover["row_data"]["formats"],
        cover["row_last"]["formats"],
    ]
    setting_dict = {}
    setting_dict["column_width_dict"] = column_width_dict
    setting_dict["row_height_list"] = row_height_list
    setting_dict["row_content_list"] = row_content_list
    setting_dict["row_format_list"] = row_format_list
    return setting_dict

    pass


def set_row_format_list(
    wb1: Workbook,
    row_format_list: dict,
):
    wb_row_format_list = []
    for i, v in enumerate(row_format_list):
        if i != 3:
            wb_row_format_list.append(wb1.add_format(v[0]))
        else:
            wb_row_format_list.append([wb1.add_format(v[0]), wb1.add_format(v[1])])

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
    for i, v in enumerate(row_height_list[:3]):
        ws1.set_row(i, v)
        row_height_list_for_break.append(v)
    row_content_list = setting_dict["row_content_list"]
    row_format_list = set_row_format_list(wb1, setting_dict["row_format_list"])
    row_index = 0
    ws1.merge_range(
        row_index,
        0,
        row_index,
        2,
        row_content_list[row_index][0],
        row_format_list[row_index],
    )
    row_index += 1
    ws1.merge_range(
        row_index,
        0,
        row_index,
        2,
        row_content_list[row_index][0],
        row_format_list[row_index],
    )
    row_index += 1
    title_str = row_content_list[row_index][0]
    title_str = title_str.replace("，", ",")
    titles: list = title_str.split(",")
    row_format_3 = row_format_list[row_index]
    for i, v in enumerate(titles):
        ws1.write(row_index, i, v, row_format_3)

    data_index = row_index
    data_index += 1
    row_format_data_1 = row_format_list[data_index][0]
    row_format_data_2 = row_format_list[data_index][1]
    row_height_data = row_height_list[data_index]
    data_index += 1
    row_format_last = row_format_list[data_index]
    row_content_last = row_content_list[data_index][0]
    row_height_last = row_height_list[data_index]

    # 灶点编码: "C",收货日期: "B",小计: "H",本账单合计: "M"
    for i, row in df.iterrows():
        row_index += 1
        ws1.set_row(row_index, row_height_data)
        row_height_list_for_break.append(row_height_data)
        ws1.write(row_index, 0, row["C"], row_format_data_1)
        ws1.write(row_index, 1, row["B"], row_format_data_2)
        ws1.write(row_index, 2, row["H"], row_format_data_1)
        pass

    if not df.empty:
        v = df.loc[0, "M"]
        row_index += 1
        ws1.set_row(row_index, row_height_data)
        row_height_list_for_break.append(row_height_data)
        ws1.write(row_index, 0, f"{zd_no}汇总", row_format_data_1)
        ws1.write(row_index, 1, "", row_format_data_2)
        ws1.write(row_index, 2, v, row_format_data_1)

    row_index += 1
    ws1.set_row(row_index, row_height_last)
    row_height_list_for_break.append(row_height_last)
    ws1.write(row_index, 2, row_content_last, row_format_last)
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
    zd_class = ""
    if product_size_dict:
        zd_class = product_size_dict[zd_no]["zd_class"] + "-"
    wb1 = Workbook(
        os_path.join(output_folder_path, f"{zd_class}{zd_no}.xlsx"),
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
        stamp_cover = stamp["cover"]
        stamp["x_offset"] = stamp_cover["x_offset"]
        stamp["y_offset"] = stamp_cover["y_offset"]
        stamp["x_scale"] = stamp_cover["x_scale"]
        stamp["y_scale"] = stamp_cover["y_scale"]
        stamp["column"] = stamp_cover["column"]
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


def write_all_cover(
    key_set: set,
    df_raw: DataFrame,
    year: int,
    month: int,
    suppier: str,
    current_data: dict,
    output_folder_path,
    product_size_dict,
):
    output_folder_path = os_path.join(
        output_folder_path, global_config_data["temp_cover"]
    )
    if not os_path.isdir(output_folder_path):
        makedirs(output_folder_path)
    product_input = copy.deepcopy(current_data["product"]["input"])
    batch_size = copy.deepcopy(current_data["batch_size"])
    cover = copy.deepcopy(current_data["product"]["output"]["cover"])
    setting_dict: dict = _get_base_data(cover, year, month, suppier)
    page_margin = cover["page_margin"]
    # 灶点编码,收货日期,小计,本账单合计
    df_raw_cover = df_raw.loc[:, ["C", "B", "H", "M"]]
    df_raw_cover_unique = df_raw_cover.drop_duplicates(subset=["C", "B"], keep="first")
    for v in key_set:
        df = df_raw_cover_unique.loc[df_raw_cover_unique["C"] == v]
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
