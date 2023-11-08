from pandas import DataFrame, ExcelWriter
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
from relax.read_excel_file import get_master_column_elec

from relax.util import (
    fill_zero_2,
    fill_zero_19,
    global_elec_hide_sheet,
    get_elec_hide_sheet,
)
from copy import deepcopy
from os import path as os_path


def group_seq_no_index(calc_list: list, header_max: int, detail_max: int):
    i = 0
    current_header_count = 0
    current_detail_count = 0
    total_count = len(calc_list)
    break_list = []
    while i < total_count:
        current_header_count += 1
        current_detail_count += calc_list[i][1]
        if current_header_count > header_max or current_detail_count > detail_max:
            current_header_count = 0
            current_detail_count = 0
            i -= 1
            break_list.append(i)
        i += 1
        pass
    if break_list:
        last_index = break_list[-1]
        if last_index < total_count - 1:
            break_list.append(total_count - 1)
    return break_list


def get_tax_no(df_tax: DataFrame, prod: str):
    is_has = False
    for _, row_tax in df_tax.iterrows():
        if row_tax["A"] == prod:
            tax_percent = row_tax["B"]
            tax_code = fill_zero_19(row_tax["C"])
            is_has = True
            return tax_percent, tax_code, is_has
    if not is_has:
        return 0, "", False


def refactor_data(
    key_set: set,
    product_size_dict: dict,
    df_raw: DataFrame,
    df_tax: DataFrame,
    current_import: dict,
    year: int,
    month: int,
):
    sale_name = current_import["sale_name"]
    sale_account = current_import["sale_account"]
    product_size_dict = deepcopy(product_size_dict)
    month = fill_zero_2(month)
    # 发票流水号,发票类型,特定业务类型,是否含税,受票方自然人标识,购买方名称,证件类型,购买方纳税人识别号,购买方地址,购买方电话,购买方开户银行,购买方银行账号,备注,是否展示购买方银行账号	销售方开户行,销售方银行账号,是否展示销售方银行账号,购买方邮箱,购买方经办人姓名,购买方经办人证件类型,购买方经办人证件号码,经办人国籍(地区),经办人自然人纳税人识别号,放弃享受减按1%征收率\n,原因,收款人,复核人
    header_list: list = []
    # 发票流水号-A,项目名称-B,商品和服务税收编码-C,规格型号-D,单位-E,数量-F,单价-G,金额-H,税率-I,折扣金额-J,是否使用优惠政策-K,优惠政策类型-L,即征即退类型-M
    product_list: list = []
    calc_list: list = []
    miss_tax_list = []
    is_continue = True
    for v in key_set:
        df = df_raw.loc[df_raw["C"] == v]
        zd_dict = product_size_dict[v]
        seq_no = f"{v}-{year}{month}"
        # 共17列
        header_row = [
            seq_no,
            "普通发票",
            "",
            "",
            "",
            zd_dict["title"],
            "",
            zd_dict["tax_no"],
            "",
            "",
            "",
            "",
            zd_dict["remark"],
            "",
            sale_name,
            sale_account,
            "是",
        ]
        product_sub_list: list = []
        product_count = 0
        is_tax = 0
        for _, row in df.iterrows():
            prod = row["E"]
            tax_code = ""
            tax_percent = 0
            tax_percent, tax_code, is_has = get_tax_no(df_tax, prod)
            if not is_has:
                miss_tax_list.append(prod)
                is_continue = False
                continue
            if not is_continue:
                continue
            is_tax_free = "" if tax_percent else "免税"
            if tax_percent:
                is_tax += 1
            amt = row["J"]
            if not amt:
                continue
            product_count += 1
            # 共13列
            product_row = [
                seq_no,
                prod,
                tax_code,
                "",
                row["G"],
                row["I"],
                "",
                amt,
                tax_percent,
                "",
                "",
                is_tax_free,
                "",
            ]
            product_sub_list.append(product_row)
        header_row[3] = "是" if is_tax else "否"
        calc_list.append((seq_no, product_count))
        header_list.append(header_row)
        product_list.append(product_sub_list)

    return header_list, product_list, calc_list, miss_tax_list


def group_seq_no(break_list: list, header_list: list, product_list: list):
    slice_list = []
    if not break_list:
        slice_list.append((header_list, product_list))
        return slice_list

    for i, v in enumerate(break_list):
        if i == 0:
            slice_list.append((header_list[: v + 1], product_list[: v + 1]))
        else:
            slice_list.append(
                (
                    header_list[break_list[i - 1] + 1 : v + 1],
                    product_list[break_list[i - 1] + 1 : v + 1],
                )
            )
        pass
    return slice_list


def make_one_import_sheet(
    wb1: Workbook,
    content_list: list,
    sheet_name: str,
    header_list: list,
    index=0,
):
    row_list = header_list
    if index == 1:
        row_list += content_list
    elif index == 2:
        for v_list in content_list:
            row_list += v_list

    ws1: Worksheet = wb1.add_worksheet(sheet_name)
    for i, rows in enumerate(row_list):
        for j, v in enumerate(rows):
            ws1.write(i, j, v)
    return ws1


def make_hidden_sheet(wb1: Workbook, hidden_sheet: list[dict]):
    for d in hidden_sheet:
        ws1: Worksheet = wb1.add_worksheet(d["name"])
        content_list = d["content"]
        for i, v in enumerate(content_list):
            ws1.write(i, 0, v)
        ws1.hide()
    pass


def make_one_import(
    file_no: int,
    seq_no_list: list,
    target_path: str,
    sheet_names: list,
    sheet_header_dict: dict,
    hidden_sheet: list,
):
    header_list: list = seq_no_list[0]
    product_list: list = seq_no_list[1]
    file_name = f"批量导入_{file_no}.xlsx"
    target_file_path = os_path.join(target_path, file_name)
    wb1 = Workbook(
        target_file_path,
        options={
            # "strings_to_numbers": True,
            "constant_memory": True,
            "encoding": "utf-8",
        },
    )
    s1 = deepcopy(sheet_header_dict["S1"])
    s2 = deepcopy(sheet_header_dict["S2"])
    s3 = deepcopy(sheet_header_dict["S3"])
    s4 = deepcopy(sheet_header_dict["S4"])
    make_one_import_sheet(wb1, header_list, sheet_names[0], s1, index=1)
    make_one_import_sheet(wb1, product_list, sheet_names[1], s2, index=2)
    make_one_import_sheet(wb1, [], sheet_names[2], s3)
    make_one_import_sheet(wb1, [], sheet_names[3], s4)

    make_hidden_sheet(wb1, hidden_sheet)

    wb1.close()
    # 从内存移除
    header_list = []
    product_list = []
    pass


def merge_same_product(product_list: list):
    dict_calc: dict = {}
    new_product_list = []
    for sub_list in product_list:
        key_calc = sub_list[0][0] if sub_list and sub_list[0] else ""
        dict_calc[key_calc] = 0
        dict_zd_prod_merge = {}
        for a, b, c, d, e, f, g, h, i, j, k, l, m in sub_list:
            key = f"{b}||{e}"
            if key not in dict_zd_prod_merge:
                dict_zd_prod_merge[key] = [a, b, c, d, e, f, g, h, i, j, k, l, m]
                dict_calc[key_calc] += 1
            else:
                old = dict_zd_prod_merge[key]
                dict_zd_prod_merge[key] = [
                    a,
                    b,
                    c,
                    d,
                    e,
                    f + old[5],
                    g,
                    h + old[7],
                    i,
                    j,
                    k,
                    l,
                    m,
                ]
        new_product_list.append(list(dict_zd_prod_merge.values()))
    calc_list = [(seq, count) for seq, count in dict_calc.items()]

    return new_product_list, calc_list


def remove_from_cover_product(header_list, product_list, calc_list, detail_max):
    calc_index_list = []
    header_index_list = []
    product_index_list = []
    detail_count_over = []
    for index, value in enumerate(calc_list):
        seq, count = value
        if count > detail_max:
            calc_index_list.append(index)
            detail_count_over.append(seq.split("-", 1)[0])
            for i, v in enumerate(header_list):
                if v[0] == seq:
                    header_index_list.append(i)
            for i, sub_list in enumerate(product_list):
                if (not sub_list) or (not sub_list[0]):
                    continue
                if sub_list[0][0] == seq:
                    product_index_list.append(i)
    new_calc_list = [
        calc_list[i] for i in range(len(calc_list)) if i not in calc_index_list
    ]
    new_header_list = [
        header_list[i] for i in range(len(header_list)) if i not in header_index_list
    ]
    new_product_list = [
        product_list[i] for i in range(len(product_list)) if i not in product_index_list
    ]
    return new_calc_list, new_header_list, new_product_list, detail_count_over
    pass


def make_batch_import_elec(
    target_path: str,
    key_set: set,
    product_size_dict: dict,
    df_raw: DataFrame,
    df_tax: DataFrame,
    current_import: dict,
    year: int,
    month: int,
):
    exclude_zd_str: str = current_import["exclude_zd"]
    is_merge = current_import["is_merge"]
    include_zd_list = []
    exclude_zd_str = exclude_zd_str.replace("，", ",")
    exclude_list = exclude_zd_str.split(",")
    for v in key_set:
        if v in exclude_list:
            continue
        include_zd_list.append(v)
    detail_max = current_import["detail_max"]
    (
        header_list,
        product_list,
        calc_list,
        miss_tax_list,
    ) = refactor_data(
        include_zd_list,
        product_size_dict,
        df_raw,
        df_tax,
        current_import,
        year,
        month,
    )
    if miss_tax_list:
        return {"miss_tax_list": miss_tax_list, "detail_count_over": None}

    if is_merge:
        product_list, calc_list = merge_same_product(product_list)
        pass

    calc_list, header_list, product_list, detail_count_over = remove_from_cover_product(
        header_list, product_list, calc_list, detail_max
    )

    break_list = group_seq_no_index(calc_list, current_import["header_max"], detail_max)
    seq_no_group_list = group_seq_no(break_list, header_list, product_list)

    sheet_name_str: str = current_import["sheet_names"]
    sheet_name_str = sheet_name_str.replace("，", ",")
    sheet_name_list = sheet_name_str.split(",")
    sheet_header_dict = get_master_column_elec(sheet_name_list)

    hidden_sheet = global_elec_hide_sheet
    if not hidden_sheet:
        hidden_sheet = get_elec_hide_sheet()
    for i, v in enumerate(seq_no_group_list):
        make_one_import(
            i, v, target_path, sheet_name_list, sheet_header_dict, hidden_sheet
        )

    return {"miss_tax_list": miss_tax_list, "detail_count_over": detail_count_over}
