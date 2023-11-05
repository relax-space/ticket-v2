from pandas import read_excel, DataFrame, isnull as pd_isnull
from datetime import datetime, timedelta
from os import listdir, path as os_path
from re import search as re_search, S as re_S
from relax.util import const_re
from calendar import monthrange
import openpyxl


def read_one_product(
    product_path: str, column_name_1: str, column_sep_1: str
) -> tuple[int, int, str]:
    # 期望到货时间,供应商名称,报账日期
    usecols = column_name_1.split(column_sep_1)
    df = read_excel(product_path, usecols=usecols, nrows=1, header=1)
    dt = df[usecols[0]].values.tolist()[0]
    year = int(dt[0:4])
    month = int(dt[5:7])
    supplier = df[usecols[1]].values.tolist()[0]
    bill_date = df[usecols[2]].values.tolist()[0]
    return year, month, supplier, bill_date

    # mapping_list = {
    #     "订单编号": "A",              => 订单编号
    #     "期望到货时间": "B",          => 收货日期
    #     "灶点编码": "C",
    #     "供应商名称": "D",
    #     "商品名称": "E",              => 商品名称
    #     "单价（元）": "F",            => 单价
    #     "计量单位": "G",              => 计量单位
    #     "收验货单总金额（元）": "H",   => 小计
    #     "数量": "I",                  => 数量
    #     "小计（元）": "J",            => 金额
    #     "报账单编号": "K",
    #     "报账日期": "L",
    #     "报账金额（元）": "M",         => 本账单合计
    # }

    # 收货日期：订单基本信息:期望到货时间
    # 订单编号：订单基本信息:订单编号
    # 商品名称：商品信息:商品名称
    # 计量单位：商品信息:计量单位
    # 单价：商品信息:单价（元）
    # 数量：收验货单信息:数量
    # 金额：
    #     金额：收验货单信息:小计（元）
    #     小计：收验货单信息:收验货单总金额（元）
    #    本账单合计：支付信息:报账金额（元）


def read_all_product(product_path, usecols_str, column_sep_1, column_sep_2):
    def datetime_to_date(date_str: str) -> str:
        return f"{date_str[5:7]}月{date_str[8:10]}日"

    def get_multindex_columns(column_name: str, sep_1, sep_2):
        columns = []
        list = column_name.split(sep_1)
        for i in list:
            sub_list = i.split(sep_2)
            columns.append((sub_list[0], sub_list[1]))
        return columns

    columns = get_multindex_columns(usecols_str, column_sep_1, column_sep_2)
    # 订单编号 A, 报账单编号 K
    order_no = columns[0]
    zd_no = columns[2]
    bill_no = columns[10]
    df = read_excel(
        product_path,
        header=[0, 1],
        dtype={order_no: str, zd_no: str, bill_no: str},
    )
    df = df[columns]
    # 一共13个
    df.columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    # 订单已撤销:报账单编号为空
    df.dropna(subset=["K"], inplace=True)
    df.loc[:, "B"] = df["B"].apply(datetime_to_date)
    return df


def get_all_tax(base_file_path: str) -> DataFrame:
    df = read_excel(
        base_file_path,
        usecols=["商品名称", "税率", "税收编码"],
        dtype={"税收编码": str},
    )
    df.columns = ["A", "B", "C"]
    df.dropna(subset=["A", "C"], inplace=True)
    df["B"].fillna(0, inplace=True)
    return df


def read_one_ticket(
    ticket_mapping_path: str,
    ticket_data: dict,
) -> tuple[int, int, str]:
    ticket_mapping_data = ticket_data["mapping"]
    column_name = ticket_mapping_data["column_name"]
    column_sep = ticket_mapping_data["column_sep"]
    date_format = ticket_mapping_data["date_format"]
    # 数电票号码,销方名称,开票日期,备注
    usecols = column_name.split(column_sep)
    df = read_excel(ticket_mapping_path, usecols=usecols, nrows=1)
    dt = df[usecols[2]].values.tolist()[0]
    date = datetime.strptime(dt, date_format).replace(day=1) + timedelta(days=-1)
    year = date.year
    month = date.month
    supplier = df[usecols[1]].values.tolist()[0]
    return year, month, supplier


def get_page_size_list(
    batch_size: dict, year: int, month: int
) -> tuple[set, dict, dict]:
    last_day = monthrange(year, month)[1]

    def replace_ymd(remark: str):
        return (
            remark.replace(const_re["year"], str(year))
            .replace(const_re["month"], str(month))
            .replace(const_re["day"], str(last_day))
        )

    def page_orient(orient: str):
        if pd_isnull(orient):
            return "p"
        return "l" if "横" in orient else "p"

    is_page_size: bool = batch_size["enable"]
    use_column_str: str = batch_size["column_name"]
    size_path: str = batch_size["path"]
    if not is_page_size:
        return set(), {}, {}
    use_column_str = use_column_str.replace("，", ",")
    usecols = use_column_str.split(",")
    df = read_excel(
        size_path, usecols=usecols, dtype={usecols[0]: str, usecols[6]: str}
    )
    # 客户id-A,分区灶点-J, 开票抬头-B, 税号-C, 发票备注-D, 发票打印大小-E, 发票打印方向-F, 发票份数-G, 筹措清单打印大小-H, 筹措清单份数-I
    df.columns = ["A", "J", "B", "C", "D", "E", "F", "G", "H", "I"]
    zd_set = set()
    product_size_dict = {}
    ticket_size_dict = {}
    df.dropna(subset=["A", "J", "B", "D", "E", "G", "H", "I"], inplace=True)
    df["C"].fillna("", inplace=True)
    for _, v in df.iterrows():
        zd = v["A"]
        zd_class = v["J"]
        title = v["B"]
        tax_no = v["C"]
        remark = replace_ymd(v["D"])
        p1_size = v["E"]
        p1_orient = page_orient(v["F"])
        p1_quantity = int(v["G"])
        p2_size = v["H"]
        p2_quantity = int(v["I"])

        for i in [p1_size, p2_size]:
            if i not in ["A4", "A5"]:
                continue
        product_size_dict[zd] = {
            "zd": zd,
            "zd_class": zd_class,
            "page_size": p2_size,
            "page_quantity": p2_quantity,
            "title": title,
            "tax_no": tax_no,
            "remark": remark,
        }
        ticket_size_dict[zd] = {
            "zd": zd,
            "zd_class": zd_class,
            "page_size": p1_size,
            "page_orient": p1_orient,
            "page_quantity": p1_quantity,
        }
        zd_set.add(zd)
        pass
    return zd_set, product_size_dict, ticket_size_dict


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


def get_ticket_mapping(
    ticket_folder_path: str,
    ticket_mapping_path: str,
    ticket_data: dict,
) -> set:
    def get_zd_disuse(raw) -> str:
        # 被红冲蓝字数电票号码：23462000000003112928 红字发票信息确认单编号：46010623101000300096
        if "被红冲蓝字数电票号码" in raw:
            m1 = re_search(r"被红冲蓝字数电票号码：((?P<ticket_no>.*?)) ", raw, re_S)
            return m1.group("ticket_no")
        return ""

    def get_zd(raw, pre: str, post: str) -> str:
        # '87001灶点  2023年9月1日至2023年9月30日菜金'
        match = re_search(rf"{pre}(?P<zd>.*?){post}", raw, re_S)
        return match.group("zd")

    mapping_data = ticket_data["mapping"]
    usecols_str: str = mapping_data["column_name"]
    sheet_name: str = mapping_data["sheet_name"]
    regax_pre: str = mapping_data["regax_pre"]
    regax_post: str = mapping_data["regax_post"]
    exclude_zd_str: str = mapping_data["exclude_zd"]
    usecols_str = usecols_str.replace("，", ",")
    usecols = usecols_str.split(",")

    exclude_zd_str = exclude_zd_str.replace("，", ",")
    exclude_zd_list: list = exclude_zd_str.split(",") if exclude_zd_str else []

    file_list = listdir(ticket_folder_path)
    # "发票基础信息"
    df_mapping_dict = read_excel(
        ticket_mapping_path, sheet_name=[sheet_name], usecols=usecols
    )
    df_mapping: DataFrame = df_mapping_dict[sheet_name]
    # 数电票号码,销方名称,开票日期,备注
    # df_mapping.rename(columns={usecols[0]: "A", usecols[3]: "D"}, inplace=True)
    df_mapping.columns = ["A", "B", "C", "D"]
    disuse_ticket_no_list = []
    for _, row in df_mapping.iterrows():
        ticket_no = row["A"]
        remark = row["D"]
        if pd_isnull(remark):
            #  理论上不存在备注为空的情况，万一存在，则忽略这条异常数据
            continue
        disuse_ticket = get_zd_disuse(remark).strip()
        if disuse_ticket:
            disuse_ticket_no_list.append(ticket_no)
            disuse_ticket_no_list.append(disuse_ticket)

    mapping_list: list[tuple] = []
    zd_set = set()
    zd_dict: dict[str, int] = {}
    for _, row in df_mapping.iterrows():
        ticket_no = row["A"]
        remark = row["D"]
        if ticket_no in disuse_ticket_no_list:
            continue
        if pd_isnull(remark):
            #  理论上不存在备注为空的情况，万一存在，则忽略这条异常数据
            continue
        zd = get_zd(remark, regax_pre, regax_post).strip()
        if zd in exclude_zd_list:
            continue
        for v in file_list:
            if v.find(ticket_no) != -1:
                if zd in zd_set:
                    numb = zd_dict[zd]
                    numb += 1
                    zd_dict[zd] = numb
                    mapping_list.append((v, zd, numb))
                else:
                    mapping_list.append((v, zd, 1))
                    zd_set.add(zd)
                    zd_dict[zd] = 1
        pass
    return zd_set, mapping_list


def pivot_master_column(headers: list):
    header_1 = []
    header_2 = []
    header_3 = []
    new_headers = [header_1, header_2, header_3]
    for i, j, k in headers:
        header_1.append(i)
        header_2.append(j)
        header_3.append(k)
    return new_headers


def get_master_column_elec(sheet_names: list) -> dict:
    df = read_excel("config/电子税务局批量导入模板.xlsx", header=[0, 1, 2], sheet_name=sheet_names)
    sheet_header_dict = {}
    s1 = pivot_master_column(df[sheet_names[0]].columns.values)
    for i1, iv in enumerate(s1):
        if i1 != 0:
            continue
        pre = ""
        for i, v in enumerate(iv):
            v_new = v.strip()
            if v_new == pre:
                iv[i] = ""
            pre = v_new

    sheet_header_dict["S1"] = s1

    s2 = pivot_master_column(df[sheet_names[1]].columns.values)
    for i1, iv in enumerate(s2):
        if i1 != 0:
            continue
        pre = ""
        for i, v in enumerate(iv):
            v_new = v.strip()
            if v_new == pre:
                iv[i] = ""
            pre = v_new

    sheet_header_dict["S2"] = s2
    s3 = pivot_master_column(df[sheet_names[2]].columns.values)
    for i1, iv in enumerate(s3):
        if i1 != 0:
            continue
        pre = ""
        for i, v in enumerate(iv):
            v_new = v.strip()
            if v_new == pre:
                iv[i] = ""
            pre = v_new

    sheet_header_dict["S3"] = s3

    s4 = pivot_master_column(df[sheet_names[3]].columns.values)
    for i1, iv in enumerate(s4):
        if i1 != 0:
            continue
        pre = ""
        for i, v in enumerate(iv):
            v_new = v.strip()
            if v_new == pre:
                iv[i] = ""
            pre = v_new
    sheet_header_dict["S4"] = s4
    return sheet_header_dict


def read_bill_sum(bill_sum_path: str):
    use_column = ["灶点编码", "报账单金额"]
    df = read_excel(bill_sum_path, usecols=use_column, dtype={"灶点编码": str})
    df.drop_duplicates(inplace=True)
    df.columns = ["A", "B"]

    df.loc[:, "B"] = df["B"].apply(convert_amt)
    return df


def convert_amt(amt_str: str):
    amt_str = amt_str.replace(",", "")
    return float(amt_str)
    pass


def read_correct_zd(correct_zd_path: str):
    lst = listdir(correct_zd_path)
    zd_obj_list = {}
    for i in lst:
        zd = i.rsplit(".", 1)[0]
        zd_obj = []
        df = read_excel(os_path.join(correct_zd_path, i), header=3)
        sum = 0.0
        for _, row in df.iterrows():
            if row["序号"] == "小计":
                continue
            elif row["序号"] == "本账单合计":
                sum = float(row["金额"])
            else:
                prod = row["商品名称"]
                if pd_isnull(prod):
                    continue
                zd_obj.append(
                    (prod, float(row["单价"]), float(row["数量"]), float(row["金额"]))
                )
        zd_obj_list[zd] = {"prod_list": zd_obj, "sum": sum}
    return zd_obj_list
