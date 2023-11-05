from pandas import DataFrame
from relax.read_excel_file import read_bill_sum, read_correct_zd


def check_bill(df_bill: DataFrame, df_raw: DataFrame):
    incorrect_set = set()
    only_iter_once_set = set()
    for _, row1 in df_raw.iterrows():
        zd = row1["C"]
        if zd in only_iter_once_set:
            continue
        for _, row2 in df_bill.iterrows():
            if zd == row2["A"]:
                only_iter_once_set.add(zd)
                if row1["M"] != row2["B"]:
                    incorrect_set.add(zd)
                break
    return incorrect_set
    pass


def find_amt(prod_list, prod_raw):
    for prod, price, numb, amt in prod_list:
        if prod_raw == prod:
            return price, numb, amt
    return 0


def update_raw_df(correct_zd_path: str, df_raw: DataFrame, zd_diff: set):
    zd_obj_list = read_correct_zd(correct_zd_path)
    if not zd_obj_list:
        return
    for i, row in df_raw.iterrows():
        zd = row["C"]
        if zd not in zd_diff:
            continue
        zd_obj = zd_obj_list[zd]
        sum = zd_obj["sum"]
        # 报账金额（元）
        df_raw.loc[i, "M"] = sum
        prod_list = zd_obj["prod_list"]
        # 商品名称
        prod_raw = row["E"]
        price, numb, amt = find_amt(prod_list, prod_raw)
        df_raw.loc[i, "F"] = price
        df_raw.loc[i, "I"] = numb
        df_raw.loc[i, "J"] = amt
        pass
