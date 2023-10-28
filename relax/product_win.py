"""
商品清单
"""
from shutil import rmtree
from tkinter.font import Font

from pandas import DataFrame
from relax.product_print import make_product_file
from relax.product_cover import write_all_cover
from relax.product_detail import write_all_product
from relax.product_import import make_import_file
from relax.read_excel_file import (
    get_all_tax,
    read_one_product,
    read_all_product,
    get_page_size_list,
)
from relax.util import (
    fill_zero_2,
    get_current_data,
    get_runtime,
    global_widgets,
    global_dict_chk_var,
    global_config_data,
)
from os import path as os_path, makedirs, startfile as os_startfile
from traceback import format_exc
from tkinter import (
    BOTH,
    E,
    END,
    LEFT,
    NW,
    RIGHT,
    TOP,
    VERTICAL,
    W,
    X,
    Button,
    Checkbutton,
    Entry,
    Frame,
    Label,
    Listbox,
    Radiobutton,
    Scrollbar,
    Text,
    filedialog,
    messagebox,
)
from relax.win_data import json_data
from time import time
from relax.util_win import render_tooltip


def path_click():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return

    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    ety_product_input: Entry = global_widgets["ety_product_input"]
    ety_product_input.delete(0, END)
    ety_product_input.insert(0, file_path)
    pass


def create_click_valid():
    lst_menu: Listbox = global_widgets["lst_menu"]
    ety_supplier_name: Entry = global_widgets["ety_supplier_name"]
    ety_output_path: Entry = global_widgets["ety_output_path"]
    ety_product_input: Entry = global_widgets["ety_product_input"]
    ety_import: Entry = global_widgets["ety_import"]
    ety_page_size: Entry = global_widgets["ety_page_size"]
    ety_A4_page_height: Entry = global_widgets["ety_A4_page_height"]
    ety_A5_page_height: Entry = global_widgets["ety_A5_page_height"]
    ety_stamp: Entry = global_widgets["ety_stamp"]
    ety_X_stamp_scale_cover: Entry = global_widgets["ety_X_stamp_scale_cover"]
    ety_Y_stamp_scale_cover: Entry = global_widgets["ety_Y_stamp_scale_cover"]
    ety_X_stamp_scale_product: Entry = global_widgets["ety_X_stamp_scale_product"]
    ety_Y_stamp_scale_product: Entry = global_widgets["ety_Y_stamp_scale_product"]

    ety_sale_name: Entry = global_widgets["ety_sale_name"]
    ety_sale_account: Entry = global_widgets["ety_sale_account"]
    ety_header_max: Entry = global_widgets["ety_header_max"]
    ety_detail_max: Entry = global_widgets["ety_detail_max"]

    if not lst_menu.curselection():
        messagebox.showwarning("警告", "请先在左边选择一个模板")
        return False
    elif not ety_supplier_name.get():
        messagebox.showwarning("警告", "供应商不能为空！")
        ety_supplier_name.focus_set()
        return False
    elif not ety_output_path.get():
        messagebox.showwarning("警告", "输出文件夹路径不能为空！")
        ety_output_path.focus_set()
        return False
    elif not ety_product_input.get():
        messagebox.showwarning("警告", "商品文件路径不能为空！")
        ety_product_input.focus_set()
        return False

    elif global_dict_chk_var["_import_var"].get():
        if not ety_import.get():
            messagebox.showwarning("警告", "税率表不能为空！")
            ety_import.focus_set()
            return False
        if global_dict_chk_var["_import_var_option"].get() == "电子税务局（批量）":
            if not global_dict_chk_var["_page_size_var"].get():
                messagebox.showwarning("警告", "当选择电子税务局（批量）时，必须勾选：是否批量设置页面尺寸！")
                ety_Y_stamp_scale_product.focus_set()
                return False
            elif not ety_sale_name.get():
                messagebox.showwarning("警告", "销售方开户行，不能为空！")
                ety_sale_name.focus_set()
                return False
            elif not ety_sale_account.get():
                messagebox.showwarning("警告", "销售方银行账号，不能为空！")
                ety_sale_account.focus_set()
                return False
            elif not ety_header_max.get():
                messagebox.showwarning("警告", "发票最大行数，不能为空！")
                ety_header_max.focus_set()
                return False
            elif not ety_detail_max.get():
                messagebox.showwarning("警告", "明细最大行数，不能为空！")
                ety_detail_max.focus_set()
                return False
            else:
                max_header_count = int(ety_header_max.get())
                max_detail_count = int(ety_detail_max.get())
                if max_header_count > 100:
                    messagebox.showwarning("警告", "明细最大行数，不能超过100！")
                    ety_detail_max.focus_set()
                    return False
                elif max_detail_count > 5000:
                    messagebox.showwarning("警告", "明细最大行数，不能超过5000！")
                    ety_detail_max.focus_set()
                    return False

    elif global_dict_chk_var["_page_size_var"].get():
        if not ety_page_size.get():
            messagebox.showwarning("警告", "尺寸表不能为空！")
            ety_page_size.focus_set()
            return False
        elif not ety_A4_page_height.get():
            messagebox.showwarning("警告", "A4不能为空！")
            ety_A4_page_height.focus_set()
            return False
        elif not ety_A5_page_height.get():
            messagebox.showwarning("警告", "A5不能为空！")
            ety_A5_page_height.focus_set()
            return False
    elif global_dict_chk_var["_stamp_var"].get():
        if not ety_stamp.get():
            messagebox.showwarning("警告", "印章路径不能为空！")
            ety_stamp.focus_set()
            return False
        elif not ety_X_stamp_scale_cover.get():
            messagebox.showwarning("警告", "宽度缩放不能为空！")
            ety_X_stamp_scale_cover.focus_set()
            return False
        elif not ety_Y_stamp_scale_cover.get():
            messagebox.showwarning("警告", "高度缩放不能为空！")
            ety_Y_stamp_scale_cover.focus_set()
            return False
        elif not ety_X_stamp_scale_product.get():
            messagebox.showwarning("警告", "宽度缩放不能为空！")
            ety_X_stamp_scale_product.focus_set()
            return False
        elif not ety_Y_stamp_scale_product.get():
            messagebox.showwarning("警告", "高度缩放不能为空！")
            ety_Y_stamp_scale_product.focus_set()
            return False

    return True


def create_click_raw(only_zd_list: list):
    t1 = time()

    if not create_click_valid():
        return

    lst_menu: Listbox = global_widgets["lst_menu"]
    ety_supplier_name: Entry = global_widgets["ety_supplier_name"]

    key = lst_menu.get(lst_menu.curselection()[0])
    current_data = get_current_data(key)
    json_data(current_data)

    product_input = current_data["product"]["input"]
    column_name_1 = product_input["column_name_1"]
    column_sep_1: str = product_input["column_sep_1"]
    product_path = product_input["product_path"]
    year, month, suppier, bill_date = read_one_product(
        product_path, column_name_1, column_sep_1
    )
    if not year or not month or not suppier:
        messagebox.showwarning(
            "警告",
            "读取文件异常，请确认以下列名是否存在：订单编号,期望到货时间,灶点编码,供应商名称,商品名称,单价（元）,计量单位,收验货单总金额（元）,数量,小计（元）,报账单编号,报账日期,报账金额（元）",
        )
        return
    supplier_name = ety_supplier_name.get()
    if suppier != supplier_name:
        messagebox.showwarning(
            "警告",
            "供应商名字不一致：文件中和界面上的供应商名字不一致，请确认!",
        )
        ety_supplier_name.focus()
        return

    output_folder_path = os_path.join(
        current_data["output_path"], suppier, f"{year}{fill_zero_2(month)}"
    )
    if not os_path.isdir(output_folder_path):
        makedirs(output_folder_path)
    batch_size = current_data["batch_size"]
    zd_set, product_size_dict, ticket_size_dict = get_page_size_list(
        batch_size, year, month
    )
    usecols_str: str = current_data["product"]["input"]["column_name"]
    column_sep_2: str = current_data["product"]["input"]["column_sep_2"]
    df = read_all_product(product_path, usecols_str,
                          column_sep_1, column_sep_2)
    if only_zd_list:
        df = df[df["C"].isin(only_zd_list)]
    df_set = set(df["C"].values)
    if zd_set:
        zd_difference = df_set.difference(zd_set)
        if zd_difference:
            messagebox.showwarning("警告", f"尺寸表缺少灶点号或者遗漏了必要的信息：{zd_difference}")
            return

        def remove_unuse(unuse_set: set, size_dict):
            for i in unuse_set:
                del size_dict[i]
            pass

        unuse_set = zd_set.difference(df_set)
        remove_unuse(unuse_set, product_size_dict)
        remove_unuse(unuse_set, ticket_size_dict)

    df_key_list = sorted(df_set)
    is_import = global_dict_chk_var["_import_var"].get()
    df_taxs = DataFrame()
    if is_import:
        base_file_path = current_data["product"]["output"]["import_list"]["path"]
        df_taxs = get_all_tax(base_file_path)
        df_set_tax = set(df_taxs["A"].values)
        df_set_raw_product = set(df["E"].values)
        zd_difference = df_set_raw_product.difference(df_set_tax)
        if zd_difference:
            messagebox.showwarning("警告", f"税率表缺少商品：{zd_difference}")
            return
        pass
    t2 = time()

    write_all_product(
        df_key_list,
        df,
        year,
        month,
        suppier,
        bill_date,
        current_data,
        output_folder_path,
        product_size_dict,
    )
    t3 = time()

    write_all_cover(
        df_key_list,
        df,
        year,
        month,
        suppier,
        current_data,
        output_folder_path,
        product_size_dict,
    )
    t4 = time()
    make_product_file(product_size_dict, output_folder_path)
    t5 = time()
    detail_count_over = []
    if is_import:
        detail_count_over = make_import_file(
            current_data,
            output_folder_path,
            df_taxs,
            df_key_list,
            product_size_dict,
            df,
            year,
            month,
        )
    t6 = time()
    print(
        get_runtime(t1, t2),
        get_runtime(t2, t3),
        get_runtime(t3, t4),
        get_runtime(t4, t5),
        get_runtime(t5, t6),
    )
    cover_source_path = os_path.join(
        output_folder_path, global_config_data["temp_cover"]
    )
    product_source_path = os_path.join(
        output_folder_path, global_config_data["temp_product"]
    )
    if os_path.isdir(cover_source_path):
        rmtree(cover_source_path)
    if os_path.isdir(product_source_path):
        rmtree(product_source_path)
    if detail_count_over:
        ety_detail_max = global_widgets["ety_detail_max"]
        max_detail_count = int(ety_detail_max.get())
        messagebox.showwarning(
            "批量导入提示",
            f"批量导入提示：以下灶点明细超过最大条数({max_detail_count})，请单独导入：{detail_count_over}",
        )
    else:
        result = messagebox.askquestion("提示", "成功，你需要打开文件夹吗？")
        if result == "yes":
            os_startfile(output_folder_path)


def create_click():
    try:
        create_click_raw([])
    except Exception as e:
        messagebox.showerror("错误", format_exc())


def single_create():
    try:
        ety_zd_input: Entry = global_widgets["ety_zd_input"]
        zd_input_str = ety_zd_input.get()
        if not zd_input_str:
            messagebox.showwarning("警告", "灶点号不能为空！")
            ety_zd_input.focus_set()
            return
        if not create_click_valid():
            return
        zd_input_str = zd_input_str.replace("，", ",")
        only_zd_list: list = zd_input_str.split(",")
        create_click_raw(only_zd_list)
    except Exception as e:
        messagebox.showerror("错误", format_exc())
        pass


def import_click():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    ety_import: Entry = global_widgets["ety_import"]
    ety_import.delete(0, END)
    ety_import.insert(0, file_path)
    pass


def stamp_click():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    ety_stamp: Entry = global_widgets["ety_stamp"]
    ety_stamp.delete(0, END)
    ety_stamp.insert(0, file_path)
    pass


def fr_top_1(fr_product_top):
    fr_0 = Frame(fr_product_top)
    lbl_product_input = Label(fr_0, text="商品文件路径:*", fg="red")
    btn1, img1 = render_tooltip(fr_0, 'asset/question.png',
                                '只会读取excel的第一个sheet！', (15, 15))
    ety_product_input = Entry(fr_0, width=60)
    btn_product_input = Button(fr_0, text="选择", command=path_click)

    lbl_product_input.grid(row=0, column=0, sticky=E, padx=(0, 0))
    btn1.grid(row=0, column=1)
    btn1.image = img1
    ety_product_input.grid(row=0, column=2, padx=(10, 0))
    btn_product_input.grid(row=0, column=3)

    global_widgets["ety_product_input"] = ety_product_input
    global_widgets["btn_product_input"] = btn_product_input
    return fr_0


def fr_top_2(fr_product_top):
    fr_0 = Frame(fr_product_top)
    chk_import = Checkbutton(
        fr_0, text="是否批量生成导入列表：", variable=global_dict_chk_var["_import_var"]
    )
    lbl_remark_1 = Label(fr_0, text="(如果不勾选，下面的设置不会生效)")
    chk_import.grid(row=0, column=0)
    lbl_remark_1.grid(row=0, column=1)
    global_widgets["chk_import"] = chk_import
    return fr_0

    pass


def fr_top_3(fr_product_top):
    fr_0 = Frame(fr_product_top)

    def rdo_click_1():
        fr_batch_info: Frame = global_widgets["fr_batch_info"]
        fr_batch_info.grid(row=4, column=0, sticky=W)
        pass

    def rdo_click_2():
        fr_batch_info: Frame = global_widgets["fr_batch_info"]
        if fr_batch_info.winfo_viewable():
            fr_batch_info.grid_forget()
        pass

    lbl_import_option = Label(fr_0, text="导入模板：")
    rdo_import_option_1 = Radiobutton(
        fr_0,
        text="电子税务局（批量）",
        value="电子税务局（批量）",
        variable=global_dict_chk_var["_import_var_option"],
        command=rdo_click_1,
    )
    rdo_import_option_2 = Radiobutton(
        fr_0,
        text="电子税务局",
        value="电子税务局",
        variable=global_dict_chk_var["_import_var_option"],
        command=rdo_click_2,
    )
    rdo_import_option_3 = Radiobutton(
        fr_0,
        text="诺诺",
        value="诺诺",
        variable=global_dict_chk_var["_import_var_option"],
        command=rdo_click_2,
    )
    lbl_import_option.grid(row=0, column=0, sticky=E, padx=(40, 0))
    rdo_import_option_1.grid(row=0, column=1)
    rdo_import_option_2.grid(row=0, column=2, padx=(20, 0))
    rdo_import_option_3.grid(row=0, column=3, padx=(20, 0))

    return fr_0

    pass


def fr_top_4(fr_product_top):
    fr_0 = Frame(fr_product_top)
    lbl_import = Label(fr_0, text="税率表:")
    btn1, img1 = render_tooltip(fr_0, 'asset/question.png',
                                '只会读取excel的第一个sheet！', (15, 15))
    ety_import = Entry(fr_0, width=60)
    btn_import = Button(fr_0, text="选择", command=import_click)

    lbl_import.grid(row=0, column=0, sticky=E, padx=(50, 0))
    btn1.grid(row=0, column=1)
    btn1.image = img1
    ety_import.grid(row=0, column=2, padx=(10, 0))
    btn_import.grid(row=0, column=3)

    global_widgets["ety_import"] = ety_import
    global_widgets["btn_import"] = btn_import
    return fr_0
    pass


def fr_top_5(fr_product_top):
    fr_batch_info = Frame(fr_product_top)
    fr_0 = Frame(fr_batch_info)
    lbl_sale = Label(fr_0, text="销售方：")
    lbl_sale_name = Label(fr_0, text="开户行：")
    ety_sale_name = Entry(fr_0, width=20)
    lbl_sale_account = Label(fr_0, text="银行账号：")
    ety_sale_account = Entry(fr_0, width=21)

    lbl_sale.grid(row=0, column=0, sticky=E, padx=(67, 0))
    lbl_sale_name.grid(row=0, column=1)
    ety_sale_name.grid(row=0, column=2)
    lbl_sale_account.grid(row=0, column=3, padx=(10, 0))
    ety_sale_account.grid(row=0, column=4)

    fr_1 = Frame(fr_batch_info)
    lbl_exclude_zd = Label(fr_1, text="排除灶点号:")
    btn2, img1 = render_tooltip(fr_1, 'asset/question.png',
                                '多个灶点用逗号分隔！', (15, 15))
    ety_exclude_zd = Entry(fr_1, width=60)

    lbl_exclude_zd.grid(row=0, column=0, sticky=E, padx=(34, 0), pady=(3, 0))
    btn2.grid(row=0, column=1)
    btn2.image = img1
    ety_exclude_zd.grid(row=0, column=2, padx=(2, 0), pady=(3, 0))

    fr_2 = Frame(fr_batch_info)
    lbl_total = Label(fr_2, text="行数限制：")
    lbl_header_max = Label(fr_2, text="发票最大行数：")
    ety_header_max = Entry(fr_2, width=10, justify=RIGHT)
    lbl_detail_max = Label(fr_2, text="明细最大行数：")
    ety_detail_max = Entry(fr_2, width=10, justify=RIGHT)

    lbl_total.grid(row=0, column=0, sticky=E, padx=(54, 0), pady=(3, 0))
    lbl_header_max.grid(row=0, column=1, pady=(3, 0))
    ety_header_max.grid(row=0, column=2, pady=(3, 0))
    lbl_detail_max.grid(row=0, column=3, padx=(10, 0), pady=(3, 0))
    ety_detail_max.grid(row=0, column=4, pady=(3, 0))

    fr_0.grid(row=0, column=0, sticky=W)
    fr_1.grid(row=1, column=0, sticky=W)
    fr_2.grid(row=2, column=0, sticky=W)

    global_widgets["ety_sale_name"] = ety_sale_name
    global_widgets["ety_sale_account"] = ety_sale_account
    global_widgets["ety_exclude_zd"] = ety_exclude_zd
    global_widgets["ety_header_max"] = ety_header_max
    global_widgets["ety_detail_max"] = ety_detail_max
    global_widgets["fr_batch_info"] = fr_batch_info

    return fr_batch_info

    pass


def fr_top_6(fr_product_top):
    fr_0 = Frame(fr_product_top)
    chk_stamp = Checkbutton(
        fr_0, text="是否批量加盖电子印章：", variable=global_dict_chk_var["_stamp_var"]
    )
    lbl_remark_3 = Label(fr_0, text="(如果不勾选，下面的设置不会生效)")
    chk_stamp.grid(row=0, column=0)
    lbl_remark_3.grid(row=0, column=1)
    global_widgets["chk_stamp"] = chk_stamp
    return fr_0
    pass


def fr_top_7(fr_product_top):
    fr_0 = Frame(fr_product_top)
    lbl_stamp = Label(fr_0, text="印章路径：")
    ety_stamp = Entry(fr_0, width=60)
    btn_stamp = Button(fr_0, text="选择", command=stamp_click)

    lbl_stamp.grid(row=0, column=0, padx=(50, 0))
    ety_stamp.grid(row=0, column=1)
    btn_stamp.grid(row=0, column=2)
    global_widgets["ety_stamp"] = ety_stamp
    global_widgets["btn_stamp"] = btn_stamp
    return fr_0
    pass


def fr_top_8(fr_product_top):
    fr_0 = Frame(fr_product_top)

    lbl_stamp_scale_cover = Label(fr_0, text="封面缩放：")
    lbl_X_stamp_scale_cover = Label(fr_0, text="宽度缩放：")
    ety_X_stamp_scale_cover = Entry(fr_0, width=6, justify=RIGHT)
    lbl_Y_stamp_scale_cover = Label(fr_0, text="高度缩放：")
    ety_Y_stamp_scale_cover = Entry(fr_0, width=6, justify=RIGHT)

    lbl_stamp_scale_cover.grid(row=0, column=0, padx=(50, 0))
    lbl_X_stamp_scale_cover.grid(row=0, column=1)
    ety_X_stamp_scale_cover.grid(row=0, column=2)
    lbl_Y_stamp_scale_cover.grid(row=0, column=3)
    ety_Y_stamp_scale_cover.grid(row=0, column=4)
    global_widgets["ety_X_stamp_scale_cover"] = ety_X_stamp_scale_cover
    global_widgets["ety_Y_stamp_scale_cover"] = ety_Y_stamp_scale_cover
    return fr_0
    pass


def fr_top_9(fr_product_top):
    fr_0 = Frame(fr_product_top)
    lbl_stamp_scale_product = Label(fr_0, text="商品缩放：")
    lbl_X_stamp_scale_product = Label(fr_0, text="宽度缩放：")
    ety_X_stamp_scale_product = Entry(fr_0, width=6, justify=RIGHT)
    lbl_Y_stamp_scale_product = Label(fr_0, text="高度缩放：")
    ety_Y_stamp_scale_product = Entry(fr_0, width=6, justify=RIGHT)

    lbl_stamp_scale_product.grid(row=0, column=0, padx=(50, 0))
    lbl_X_stamp_scale_product.grid(row=0, column=1)
    ety_X_stamp_scale_product.grid(row=0, column=2)
    lbl_Y_stamp_scale_product.grid(row=0, column=3)
    ety_Y_stamp_scale_product.grid(row=0, column=4)
    global_widgets["ety_X_stamp_scale_product"] = ety_X_stamp_scale_product
    global_widgets["ety_Y_stamp_scale_product"] = ety_Y_stamp_scale_product
    return fr_0
    pass


def fr_top(fr_product_top):
    row_index = 0
    fr_1 = fr_top_1(fr_product_top)
    fr_1.grid(row=row_index, column=0, sticky=W)

    row_index += 1
    fr_2 = fr_top_2(fr_product_top)
    fr_2.grid(row=row_index, column=0, sticky=W)

    row_index += 1
    fr_3 = fr_top_3(fr_product_top)
    fr_3.grid(row=row_index, column=0, sticky=W)

    row_index += 1
    fr_4 = fr_top_4(fr_product_top)
    fr_4.grid(row=row_index, column=0, sticky=W)

    fr_5 = fr_top_5(fr_product_top)
    row_index += 1
    fr_5.grid(row=row_index, column=0, sticky=W)

    fr_6 = fr_top_6(fr_product_top)
    row_index += 1
    fr_6.grid(row=row_index, column=0, sticky=W)

    fr_7 = fr_top_7(fr_product_top)
    row_index += 1
    fr_7.grid(row=row_index, column=0, sticky=W)

    fr_8 = fr_top_8(fr_product_top)
    row_index += 1
    fr_8.grid(row=row_index, column=0, sticky=W)

    fr_9 = fr_top_9(fr_product_top)
    row_index += 1
    fr_9.grid(row=row_index, column=0, sticky=W)

    btn_product_create = Button(
        fr_product_top, text='生成', width=10, command=create_click)
    btn_product_create.grid(
        row=0,
        column=1,
        rowspan=4,
        padx=(40, 0),
        pady=(20, 20),
        sticky="W" + "E" + "N" + "S",
    )

    pass


def fr_cover(fr_product_bottom_1: Frame):
    fr_1 = Frame(fr_product_bottom_1, height=25)

    lbl_1 = Label(fr_1, text="封面设置")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))
    lbl_1.pack(side=TOP)
    fr_1.pack(side=TOP, anchor=NW)

    fr_2 = Frame(fr_product_bottom_1)
    lbl_column_width_title = Label(fr_2, text=f"列宽：")
    lbl_column_width_title.pack(side=TOP)

    list = ("A", "B", "C")
    for i in list:
        lbl_column_width = Label(fr_2, text=f"{i}:")
        ety_column_width = Entry(fr_2, width=6, justify=RIGHT)
        global_widgets[f"lbl_column_width_cover_{i}"] = lbl_column_width
        global_widgets[f"ety_column_width_cover_{i}"] = ety_column_width

    column_index = 0
    lbl_column_width_title.grid(
        row=0, column=column_index, padx=(20, 0), sticky=E)
    column_index += 1
    for v in list:
        lbl_column_width: Label = global_widgets[f"lbl_column_width_cover_{v}"]
        ety_column_width: Entry = global_widgets[f"ety_column_width_cover_{v}"]
        lbl_column_width.grid(row=0, column=column_index,
                              sticky=E, padx=(0, 2))
        column_index += 1
        ety_column_width.grid(row=0, column=column_index, padx=(3, 2))
        column_index += 1

    fr_2.pack(side=TOP, anchor=NW)

    fr_3 = Frame(fr_product_bottom_1)
    lbl_row_height_title = Label(fr_3, text=f"行高：")
    list = ("第一行", "第二行", "第三行", "数据行", "盖章行")
    for i, v in enumerate(list):
        lbl_row_height = Label(fr_3, text=f"{v}:")
        ety_row_height = Entry(fr_3, width=3, justify=RIGHT)
        global_widgets[f"lbl_row_height_cover_{i}"] = lbl_row_height
        global_widgets[f"ety_row_height_cover_{i}"] = ety_row_height

    column_index = 0
    lbl_row_height_title.grid(
        row=0, column=column_index, padx=(20, 0), sticky=E)
    column_index += 1
    for i, v in enumerate(list):
        lbl_row_height: Label = global_widgets[f"lbl_row_height_cover_{i}"]
        ety_row_height: Entry = global_widgets[f"ety_row_height_cover_{i}"]
        lbl_row_height.grid(row=0, column=column_index, sticky=E, padx=(0, 2))
        column_index += 1
        ety_row_height.grid(row=0, column=column_index, padx=(3, 2))
        column_index += 1

    fr_3.pack(fill=BOTH, pady=(3, 0))
    pass


def fr_product(fr_product_bottom_2):
    fr_1 = Frame(fr_product_bottom_2, height=25)

    lbl_1 = Label(fr_1, text="商品设置")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))
    lbl_1.pack(side=TOP)
    fr_1.pack(side=TOP, anchor=NW)

    fr_2 = Frame(fr_product_bottom_2)
    lbl_column_width_title = Label(fr_2, text=f"列宽：")

    list = ("A", "B", "C", "D", "E", "F", "G", "H")
    for i in list:
        lbl_column_width = Label(fr_2, text=f"{i}:")
        ety_column_width = Entry(fr_2, width=6, justify=RIGHT)
        global_widgets[f"lbl_column_width_product_{i}"] = lbl_column_width
        global_widgets[f"ety_column_width_product_{i}"] = ety_column_width

    column_index = 0
    lbl_column_width_title.grid(
        row=0, column=column_index, padx=(20, 0), sticky=E)
    column_index += 1
    for v in list:
        lbl_column_width: Label = global_widgets[f"lbl_column_width_product_{v}"]
        ety_column_width: Entry = global_widgets[f"ety_column_width_product_{v}"]
        lbl_column_width.grid(row=0, column=column_index,
                              sticky=E, padx=(0, 2))
        column_index += 1
        ety_column_width.grid(row=0, column=column_index, padx=(0, 10))
        column_index += 1

    fr_2.pack(side=TOP, anchor=NW)

    fr_3 = Frame(fr_product_bottom_2)
    lbl_row_height_title = Label(fr_3, text=f"行高：")
    list = ("第一行", "第二行", "第三行", "第四行", "数据行", "汇总行1", "汇总行2", "盖章行")
    for i, v in enumerate(list):
        lbl_row_height = Label(fr_3, text=f"{v}:")
        ety_row_height = Entry(fr_3, width=3, justify=RIGHT)
        global_widgets[f"lbl_row_height_product_{i}"] = lbl_row_height
        global_widgets[f"ety_row_height_product_{i}"] = ety_row_height

    column_index = 0
    lbl_row_height_title.grid(
        row=0, column=column_index, padx=(20, 0), sticky=E)
    column_index += 1
    for i, v in enumerate(list):
        lbl_row_height: Label = global_widgets[f"lbl_row_height_product_{i}"]
        ety_row_height: Entry = global_widgets[f"ety_row_height_product_{i}"]
        lbl_row_height.grid(row=0, column=column_index, sticky=E, padx=(0, 2))
        column_index += 1
        ety_row_height.grid(row=0, column=column_index, padx=(3, 2))
        column_index += 1

    fr_3.pack(fill=BOTH, pady=(3, 0))
    pass


def fr_special_zd(fr_product_bottom_3: Frame):
    fr_1 = Frame(fr_product_bottom_3, height=25)

    lbl_1 = Label(fr_1, text="生成 - 个别灶点")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))
    lbl_1.pack(side=TOP)
    fr_1.pack(side=TOP, anchor=NW)

    fr_2 = Frame(fr_product_bottom_3)
    fr_2.pack(side=TOP, anchor=NW)
    lbl_zd_title = Label(fr_2, text=f"灶点号:")
    btn1, img1 = render_tooltip(fr_2, 'asset/question.png',
                                '多个灶点用逗号分隔！', (15, 15))
    ety_zd_input = Entry(fr_2, width=60)
    btn_zd_input = Button(fr_2, text="个别生成", command=single_create)

    row_index = 0
    lbl_zd_title.grid(row=row_index, column=0, padx=(20, 0), sticky=E)
    btn1.grid(row=row_index, column=2)
    btn1.image = img1
    ety_zd_input.grid(row=row_index, column=3, padx=(5, 0))
    btn_zd_input.grid(row=row_index, column=4)
    global_widgets["ety_zd_input"] = ety_zd_input
    pass


def fr_log(fr_product_bottom_3):
    fr_1 = Frame(fr_product_bottom_3, height=20)
    fr_2 = Frame(fr_product_bottom_3)
    lbl_1 = Label(fr_1, text="执行日志")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))
    txt_product_log = Text(fr_2)
    slb = Scrollbar(orient=VERTICAL, command=txt_product_log.yview)
    txt_product_log.configure(yscrollcommand=slb.set, state="disabled")

    lbl_1.pack(side=LEFT, fill=X)
    txt_product_log.pack(fill=BOTH, expand=True, padx=10, pady=(3, 0))
    fr_1.pack(side=TOP, fill=X)
    fr_2.pack(fill=BOTH, expand=True)

    global_widgets["txt_product_log"] = txt_product_log
    pass


def fr_bottom(fr_product_bottom: Frame):
    fr_input_sep_1 = Frame(fr_product_bottom, height=2,
                           borderwidth=1, relief="groove")
    fr_input_sep_1.pack(side=TOP, fill=X, padx=3, pady=5)

    fr_product_bottom_1 = Frame(fr_product_bottom, height=80)
    fr_product_bottom_1.pack(side=TOP, anchor=NW)

    fr_product_bottom_2 = Frame(fr_product_bottom, height=80)
    fr_product_bottom_2.pack(side=TOP, anchor=NW)

    fr_product_bottom_3 = Frame(fr_product_bottom, height=80)
    fr_product_bottom_3.pack(side=TOP, anchor=NW)

    fr_cover(fr_product_bottom_1)
    fr_product(fr_product_bottom_2)
    fr_special_zd(fr_product_bottom_3)

    pass


def init_fr_product():
    fr_product: Frame = global_widgets["fr_product"]
    fr_product_top = Frame(fr_product)
    fr_product_bottom = Frame(fr_product)
    global_widgets["fr_product_top"] = fr_product_top
    global_widgets["fr_product_bottom"] = fr_product_bottom

    fr_product_top.pack(side=TOP, fill=X)
    fr_product_bottom.pack(fill=BOTH, expand=True)

    fr_top(fr_product_top)
    fr_bottom(fr_product_bottom)

    pass


if __name__ == "__main__":
    pass
