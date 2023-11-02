from pandas import DataFrame, isna
from relax.batch_import_master import make_batch_import_elec
from relax.read_excel_file import read_product
from relax.util import global_dict_chk_var, global_config_data, fill_zero_19
from os import listdir, path as os_path, makedirs


def make_import_one_nuonuo(
    df_taxs,
    source_path,
    target_path,
    file_name,
    row_info: dict,
    product_titles,
):
    df = read_product(os_path.join(source_path, file_name), product_titles)
    columns = row_info["row1_content"]
    rows = [row_info["row2_content"], row_info["row3_content"]]
    # 序号A,收货日期B,订单编号C,商品名称D,计量单位E,单价F,数量G,金额H
    for _, row in df.iterrows():
        cond = row["A"]
        if isna(cond):
            continue
        if not str.isdecimal(cond):
            continue
        if not row["H"]:
            continue
        new_row = []
        prod = row["D"].replace("\n", "")
        df_tax = df_taxs.loc[df_taxs["A"] == prod]
        new_row.append(prod)
        new_row.append("")
        new_row.append(row["E"])
        new_row.append(row["G"])
        new_row.append("")
        new_row.append(row["H"])

        tax_percent = df_tax["B"].values[0]
        is_tax_free = "" if tax_percent else "免税"
        new_row.append(tax_percent)
        new_row.append(df_tax["C"].values[0])
        new_row.append(is_tax_free)
        rows.append(new_row)
    DataFrame(rows, columns=columns).to_excel(
        target_path, startrow=0, index=False)
    pass


def make_import_one_elec(
    df_taxs,
    source_path,
    target_path,
    file_name,
    row_info: dict,
    product_titles: list,
):
    df = read_product(os_path.join(source_path, file_name), product_titles)
    columns = row_info["row1_content"]
    rows = [row_info["row2_content"], row_info["row3_content"]]
    # 序号A,收货日期B,订单编号C,商品名称D,计量单位E,单价F,数量G,金额H
    for _, row in df.iterrows():
        cond = row["A"]
        if isna(cond):
            continue
        if not str.isdecimal(cond):
            continue
        if not row["H"]:
            continue
        new_row = []
        prod = row["D"].replace("\n", "")
        df_tax = df_taxs.loc[df_taxs["A"] == prod]
        new_row.append(prod)
        tax_percent = df_tax["B"].values[0]
        is_tax_free = "" if tax_percent else "免税"
        new_row.append(fill_zero_19(df_tax["C"].values[0]))
        new_row.append("")
        new_row.append(row["E"])
        new_row.append(row["G"])
        new_row.append("")
        new_row.append(row["H"])

        new_row.append(tax_percent)
        new_row.append("")
        new_row.append(is_tax_free)
        rows.append(new_row)
    DataFrame(rows, columns=columns).to_excel(
        target_path, startrow=0, index=False)


def make_import_file(
    current_data: dict,
    output_folder_path: str,
    df_tax: DataFrame,
    key_set: set,
    product_size_dict: dict,
    df_raw: DataFrame,
    year: int,
    month: int,
):
    output_product = current_data["product"]["output"]
    import_list = output_product["import_list"]

    product_path = os_path.join(
        output_folder_path, global_config_data["temp_product"])
    temp_cover = os_path.join(
        output_folder_path, global_config_data["temp_cover"])
    target_path = os_path.join(
        output_folder_path, global_config_data["import_list"])

    product_title_str: str = output_product["product_detail"]["row4"]["contents"][0]
    product_title_str = product_title_str.replace("，", ",")
    product_titles = product_title_str.split(",")

    v = global_dict_chk_var["_import_var_option"].get()
    if v == "诺诺":
        current_import = import_list[v]
        target_path = os_path.join(target_path, v)
        if not os_path.isdir(target_path):
            makedirs(target_path)
        files = listdir(product_path)
        for i in files:
            target_file_path = os_path.join(target_path, i)
            make_import_one_nuonuo(
                df_tax,
                product_path,
                target_file_path,
                i,
                current_import,
                product_titles,
            )
        return None
        pass
    elif v == "电子税务局":
        current_import = import_list[v]
        target_path = os_path.join(target_path, v)
        if not os_path.isdir(target_path):
            makedirs(target_path)
        files = listdir(product_path)
        for i in files:
            target_file_path = os_path.join(target_path, i)
            make_import_one_elec(
                df_tax,
                product_path,
                target_file_path,
                i,
                current_import,
                product_titles,
            )
        return None
        pass
    elif v == "电子税务局（批量）":
        target_path = os_path.join(target_path, v)
        if not os_path.isdir(target_path):
            makedirs(target_path)
        current_import = import_list[v]
        return make_batch_import_elec(
            target_path,
            key_set,
            product_size_dict,
            df_raw,
            df_tax,
            current_import,
            year,
            month,
        )
        pass

    pass
