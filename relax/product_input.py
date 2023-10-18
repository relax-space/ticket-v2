from pandas import read_excel


def get_multindex_columns(column_name: str, sep_1, sep_2):
    columns = []
    list = column_name.split(sep_1)
    for i in list:
        sub_list = i.split(sep_2)
        columns.append((sub_list[0], sub_list[1]))
    return columns

    pass


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
    columns = get_multindex_columns(usecols_str, column_sep_1, column_sep_2)
    # 订单编号 A, 报账单编号 K
    order_no = columns[0]
    bill_no = columns[10]
    df = read_excel(
        product_path, header=[0, 1], dtype={order_no: "str", bill_no: "str"}
    )
    df = df[columns]
    df.columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    # 一共13个
    return df
