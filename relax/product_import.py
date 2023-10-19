from pandas import DataFrame, read_excel, isna
from relax.product_input import get_all_base
from relax.util import global_dict_chk_var, global_config_data
from os import listdir, path as os_path, makedirs


def read_product(product_folder_path: str, columns: str):
    df = read_excel(product_folder_path, header=3, dtype={"序号": str})
    # 序号A,收货日期B,订单编号C,商品名称D,计量单位E,单价F,数量G,金额H
    df.rename(
        columns={
            columns[0]: "A",
            columns[1]: "B",
            columns[2]: "C",
            columns[3]: "D",
            columns[4]: "E",
            columns[5]: "F",
            columns[6]: "G",
            columns[7]: "H",
        },
        inplace=True,
    )
    return df


def make_import_one_nuonuo(
    df_bases,
    set1,
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
        new_row = []
        prod = row["D"].replace("\n", "")
        df_base = df_bases.loc[df_bases["商品名称"] == prod]
        new_row.append(prod)
        new_row.append("")
        new_row.append(row["E"])
        new_row.append(row["G"])
        new_row.append("")
        new_row.append(row["H"])

        if df_base.empty:
            set1.add(prod)
            new_row.append("没有找到")
            new_row.append("")
            new_row.append("")
        else:
            new_row.append(df_base["税率"].fillna("0.0").values[0])
            new_row.append(df_base["税收编码"].fillna("").values[0])
            new_row.append(df_base["免税"].fillna("").values[0])
        rows.append(new_row)
    DataFrame(rows, columns=columns).to_excel(target_path, startrow=0, index=False)
    pass


def make_import_one_elec(
    df_bases,
    set1,
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
        new_row = []
        prod = row["D"].replace("\n", "")
        df_base = df_bases.loc[df_bases["商品名称"] == prod]
        new_row.append(prod)
        if df_base.empty:
            new_row.append("")
        else:
            new_row.append(df_base["税收编码"].fillna("").values[0])
        new_row.append("")
        new_row.append(row["E"])
        new_row.append(row["G"])
        new_row.append("")
        new_row.append(row["H"])

        if df_base.empty:
            set1.add(prod)
            new_row.append("没有找到")
            new_row.append("")
            new_row.append("")
        else:
            new_row.append(df_base["税率"].fillna("0.0").values[0])
            new_row.append("")
            new_row.append(df_base["免税"].fillna("").values[0])
        rows.append(new_row)
    DataFrame(rows, columns=columns).to_excel(target_path, startrow=0, index=False)


def make_import_file(current_data: dict, output_folder_path: str, df_bases: DataFrame):
    output_product = current_data["product"]["output"]
    import_list = output_product["import_list"]

    source_path = os_path.join(output_folder_path, global_config_data["temp_product"])
    target_path = os_path.join(output_folder_path, global_config_data["import_list"])

    product_title_str: str = output_product["product_detail"]["row4"]["contents"][0]
    product_titles = product_title_str.split(",")

    files = listdir(source_path)
    v = global_dict_chk_var["_import_var_option"].get()
    if v == "诺诺":
        row_info = import_list[v]
        set1 = set()
        target_path = os_path.join(target_path, v)
        if not os_path.isdir(target_path):
            makedirs(target_path)
        for i in files:
            target_file_path = os_path.join(target_path, i)
            make_import_one_nuonuo(
                df_bases,
                set1,
                source_path,
                target_file_path,
                i,
                row_info,
                product_titles,
            )
        pass
    elif v == "电子税务局":
        row_info = import_list[v]
        set1 = set()
        target_path = os_path.join(target_path, v)
        if not os_path.isdir(target_path):
            makedirs(target_path)
        for i in files:
            target_file_path = os_path.join(target_path, i)
            make_import_one_elec(
                df_bases,
                set1,
                source_path,
                target_file_path,
                i,
                row_info,
                product_titles,
            )
        pass

    pass
