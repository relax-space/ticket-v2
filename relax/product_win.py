"""
商品清单
"""
import time
from tkinter.font import Font

from pandas import DataFrame
from relax.excel_common import get_page_size_list
from relax.product_cover import write_all_cover
from relax.product_detail import write_all_product
from relax.product_import import make_import_file
from relax.product_input import get_all_base, read_one_product, read_all_product
from relax.product_print import make_product_file
from relax.util import (
    fill_zero_2,
    get_current_data,
    global_widgets,
    global_dict_chk_var,
)
from os import path as os_path, makedirs
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


def create_click_raw():
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

    def create_click_valid():
        if not lst_menu.curselection():
            messagebox.showwarning("警告", "请先在左边选择一个模板")
            return False

        if not ety_supplier_name.get():
            messagebox.showwarning("警告", "供应商不能为空！")
            ety_supplier_name.focus_set()
            return False
        if not ety_output_path.get():
            messagebox.showwarning("警告", "输出文件夹路径不能为空！")
            ety_output_path.focus_set()
            return False
        if not ety_product_input.get():
            messagebox.showwarning("警告", "商品文件路径不能为空！")
            ety_product_input.focus_set()
            return False

        if global_dict_chk_var["_import_var"] and not ety_import.get():
            messagebox.showwarning("警告", "税率表不能为空！")
            ety_import.focus_set()
            return False
        if global_dict_chk_var["_page_size_var"]:
            if not ety_page_size.get():
                messagebox.showwarning("警告", "尺寸表不能为空！")
                ety_page_size.focus_set()
                return False
            if not ety_A4_page_height.get():
                messagebox.showwarning("警告", "A4不能为空！")
                ety_A4_page_height.focus_set()
                return False
            if not ety_A5_page_height.get():
                messagebox.showwarning("警告", "A5不能为空！")
                ety_A5_page_height.focus_set()
                return False
        if global_dict_chk_var["_stamp_var"]:
            if not ety_stamp.get():
                messagebox.showwarning("警告", "印章路径不能为空！")
                ety_stamp.focus_set()
                return False
            if not ety_X_stamp_scale_cover.get():
                messagebox.showwarning("警告", "宽度缩放不能为空！")
                ety_X_stamp_scale_cover.focus_set()
                return False
            if not ety_Y_stamp_scale_cover.get():
                messagebox.showwarning("警告", "高度缩放不能为空！")
                ety_Y_stamp_scale_cover.focus_set()
                return False
            if not ety_X_stamp_scale_product.get():
                messagebox.showwarning("警告", "宽度缩放不能为空！")
                ety_X_stamp_scale_product.focus_set()
                return False
            if not ety_Y_stamp_scale_product.get():
                messagebox.showwarning("警告", "高度缩放不能为空！")
                ety_Y_stamp_scale_product.focus_set()
                return False
        return True

    if not create_click_valid():
        return
    key = lst_menu.get(lst_menu.curselection()[0])
    current_data = get_current_data(key)
    json_data(current_data)

    column_name_1 = current_data["product"]["input"]["column_name_1"]
    column_sep_1: str = current_data["product"]["input"]["column_sep_1"]
    product_path = ety_product_input.get()
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
        return

    usecols_str: str = current_data["product"]["input"]["column_name"]
    column_sep_2: str = current_data["product"]["input"]["column_sep_2"]
    df = read_all_product(product_path, usecols_str, column_sep_1, column_sep_2)

    output_folder_path = os_path.join(
        current_data["output_path"], suppier, f"{year}{fill_zero_2(month)}"
    )
    if not os_path.isdir(output_folder_path):
        makedirs(output_folder_path)
    batch_size = current_data["batch_size"]
    zd_set, product_size_dict, ticket_size_dict = get_page_size_list(batch_size)
    df_set = set(df["C"].values)
    if product_size_dict:
        zd_difference = df_set.difference(zd_set)
        if zd_difference:
            messagebox.showwarning("警告", f"尺寸表缺少灶点号：{zd_difference}")
            return
    is_import = global_dict_chk_var["_import_var"]
    df_bases = DataFrame()
    if is_import:
        base_file_path = current_data["product"]["output"]["import_list"]["path"]
        df_bases = get_all_base(base_file_path)
        df_set_tax = set(df_bases["商品名称"].values)
        df_set_raw_product = set(df["E"].values)
        zd_difference = df_set_raw_product.difference(df_set_tax)
        if zd_difference:
            messagebox.showwarning("警告", f"税率表缺少商品：{zd_difference}")
            return
        pass
    write_all_product(
        df_set,
        df,
        year,
        month,
        suppier,
        bill_date,
        current_data,
        output_folder_path,
        product_size_dict,
    )

    write_all_cover(
        df_set,
        df,
        year,
        month,
        suppier,
        current_data,
        output_folder_path,
        product_size_dict,
    )
    if product_size_dict:
        make_product_file(product_size_dict, output_folder_path)

    if is_import:
        make_import_file(current_data, output_folder_path, df_bases)


def create_click():
    try:
        create_click_raw()
    except Exception as e:
        messagebox.showerror("错误", format_exc())


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


def fr_top(fr_product_top, fr_product_top_1):
    lbl_product_input = Label(fr_product_top, text="商品文件路径：*", fg="red")
    ety_product_input = Entry(fr_product_top, width=60)
    btn_product_input = Button(fr_product_top, text="选择", command=path_click)

    btn_product_create = Button(
        fr_product_top, text="生成", width=15, command=create_click
    )

    # lbl_product_output = Label(fr_product_top, text="商品输出路径：")
    # ety_product_output = Entry(fr_product_top, width=60)
    # btn_product_output = Button(fr_product_top, text="选择")

    chk_import = Checkbutton(
        fr_product_top, text="是否批量生成导入列表：", variable=global_dict_chk_var["_import_var"]
    )
    lbl_remark_1 = Label(fr_product_top, text="(如果不勾选，下面的设置不会生效)")
    lbl_import = Label(fr_product_top, text="税率表：")
    ety_import = Entry(fr_product_top, width=60)
    btn_import = Button(fr_product_top, text="选择", command=import_click)

    fr_import_option = Frame(fr_product_top)
    lbl_import_option = Label(fr_import_option, text="导入模板：")
    rdo_import_option_1 = Radiobutton(
        fr_import_option,
        text="诺诺",
        value="诺诺",
        variable=global_dict_chk_var["_import_var_option"],
    )
    rdo_import_option_2 = Radiobutton(
        fr_import_option,
        text="电子税务局",
        value="电子税务局",
        variable=global_dict_chk_var["_import_var_option"],
    )
    lbl_import_option.grid(row=0, column=0, sticky=E)
    rdo_import_option_1.grid(row=0, column=1)
    rdo_import_option_2.grid(row=0, column=2, padx=(20, 0))

    chk_stamp = Checkbutton(
        fr_product_top, text="是否盖章：", variable=global_dict_chk_var["_stamp_var"]
    )
    lbl_remark_3 = Label(fr_product_top, text="(如果不勾选，下面的设置不会生效)")
    lbl_stamp = Label(fr_product_top, text="印章路径：")
    ety_stamp = Entry(fr_product_top, width=60)
    btn_stamp = Button(fr_product_top, text="选择", command=stamp_click)

    row_index = 0
    lbl_product_input.grid(row=row_index, column=0, sticky=E, pady=(10, 3))
    ety_product_input.grid(row=row_index, column=1, pady=(10, 3), columnspan=4)
    btn_product_input.grid(row=row_index, column=5, pady=(10, 3))

    btn_product_create.grid(
        row=row_index,
        column=6,
        rowspan=4,
        padx=(40, 0),
        pady=(20, 20),
        sticky="W" + "E" + "N" + "S",
    )

    # row_index += 1
    # lbl_product_output.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    # ety_product_output.grid(row=row_index, column=1, pady=(0, 3), columnspan=4)
    # btn_product_output.grid(row=row_index, column=5, pady=(0, 3))

    row_index += 1
    chk_import.grid(row=row_index, column=0, pady=(0, 3), sticky=E)
    lbl_remark_1.grid(row=row_index, column=1, sticky="w", columnspan=4)

    row_index += 1
    lbl_import.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_import.grid(row=row_index, column=1, pady=(0, 3), columnspan=4)
    btn_import.grid(row=row_index, column=5, pady=(0, 3))

    row_index += 1
    fr_import_option.grid(row=row_index, padx=(94, 0), column=0, columnspan=2)

    row_index += 1
    chk_stamp.grid(row=row_index, column=0, pady=(0, 3), sticky=E)
    lbl_remark_3.grid(row=row_index, column=1, sticky="w", columnspan=4)
    row_index += 1
    lbl_stamp.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_stamp.grid(row=row_index, column=1, pady=(0, 3), columnspan=4)
    btn_stamp.grid(row=row_index, column=5, pady=(0, 3))

    global_widgets["ety_product_input"] = ety_product_input
    global_widgets["btn_product_input"] = btn_product_input
    # global_widgets["ety_product_output"] = ety_product_output
    global_widgets["chk_import"] = chk_import
    global_widgets["ety_import"] = ety_import
    global_widgets["btn_import"] = btn_import

    global_widgets["chk_stamp"] = chk_stamp
    global_widgets["ety_stamp"] = ety_stamp
    global_widgets["btn_stamp"] = btn_stamp

    lbl_stamp_scale_cover = Label(fr_product_top_1, text="封面缩放：")
    lbl_X_stamp_scale_cover = Label(fr_product_top_1, text="宽度缩放：")
    ety_X_stamp_scale_cover = Entry(fr_product_top_1, width=6, justify=RIGHT)
    lbl_Y_stamp_scale_cover = Label(fr_product_top_1, text="高度缩放：")
    ety_Y_stamp_scale_cover = Entry(fr_product_top_1, width=6, justify=RIGHT)

    lbl_stamp_scale_product = Label(fr_product_top_1, text="商品缩放：")
    lbl_X_stamp_scale_product = Label(fr_product_top_1, text="宽度缩放：")
    ety_X_stamp_scale_product = Entry(fr_product_top_1, width=6, justify=RIGHT)
    lbl_Y_stamp_scale_product = Label(fr_product_top_1, text="高度缩放：")
    ety_Y_stamp_scale_product = Entry(fr_product_top_1, width=6, justify=RIGHT)

    row_index = 0
    lbl_stamp_scale_cover.grid(
        row=row_index, column=0, padx=(94, 0), pady=(3, 0), sticky=E
    )
    lbl_X_stamp_scale_cover.grid(row=row_index, column=1, pady=(3, 0), sticky=W)
    ety_X_stamp_scale_cover.grid(row=row_index, column=2, pady=(3, 0), sticky=W)
    lbl_Y_stamp_scale_cover.grid(
        row=row_index, column=3, padx=(10, 0), pady=(3, 0), sticky=W
    )
    ety_Y_stamp_scale_cover.grid(row=row_index, column=4, pady=(3, 0), sticky=W)

    row_index += 1
    lbl_stamp_scale_product.grid(
        row=row_index, column=0, padx=(94, 0), pady=(3, 0), sticky=E
    )
    lbl_X_stamp_scale_product.grid(row=row_index, column=1, pady=(3, 0), sticky=W)
    ety_X_stamp_scale_product.grid(row=row_index, column=2, pady=(3, 0), sticky=W)
    lbl_Y_stamp_scale_product.grid(
        row=row_index, column=3, padx=(10, 0), pady=(3, 0), sticky=W
    )
    ety_Y_stamp_scale_product.grid(row=row_index, column=4, pady=(3, 0), sticky=W)

    global_widgets["ety_X_stamp_scale_cover"] = ety_X_stamp_scale_cover
    global_widgets["ety_Y_stamp_scale_cover"] = ety_Y_stamp_scale_cover

    global_widgets["ety_X_stamp_scale_product"] = ety_X_stamp_scale_product
    global_widgets["ety_Y_stamp_scale_product"] = ety_Y_stamp_scale_product

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
    lbl_column_width_title.grid(row=0, column=column_index, padx=(20, 0), sticky=E)
    column_index += 1
    for v in list:
        lbl_column_width: Label = global_widgets[f"lbl_column_width_cover_{v}"]
        ety_column_width: Entry = global_widgets[f"ety_column_width_cover_{v}"]
        lbl_column_width.grid(row=0, column=column_index, sticky=E, padx=(0, 2))
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
    lbl_row_height_title.grid(row=0, column=column_index, padx=(20, 0), sticky=E)
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
    lbl_column_width_title.pack(side=TOP)

    list = ("A", "B", "C", "D", "E", "F", "G", "H")
    for i in list:
        lbl_column_width = Label(fr_2, text=f"{i}:")
        ety_column_width = Entry(fr_2, width=6, justify=RIGHT)
        global_widgets[f"lbl_column_width_product_{i}"] = lbl_column_width
        global_widgets[f"ety_column_width_product_{i}"] = ety_column_width

    column_index = 0
    lbl_column_width_title.grid(row=0, column=column_index, padx=(20, 0), sticky=E)
    column_index += 1
    for v in list:
        lbl_column_width: Label = global_widgets[f"lbl_column_width_product_{v}"]
        ety_column_width: Entry = global_widgets[f"ety_column_width_product_{v}"]
        lbl_column_width.grid(row=0, column=column_index, sticky=E, padx=(0, 2))
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
    lbl_row_height_title.grid(row=0, column=column_index, padx=(20, 0), sticky=E)
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
    fr_input_sep_1 = Frame(fr_product_bottom, height=2, borderwidth=1, relief="groove")
    fr_input_sep_1.pack(side=TOP, fill=X, padx=3, pady=5)

    fr_product_bottom_1 = Frame(fr_product_bottom, height=80)
    fr_product_bottom_1.pack(side=TOP, anchor=NW)
    # fr_product_bottom_1.pack_propagate(0)

    # fr_input_sep_2 = Frame(fr_product_bottom, width=2, borderwidth=1, relief="groove")
    # fr_input_sep_2.pack(side=LEFT, fill=Y, padx=3, pady=2)

    fr_product_bottom_2 = Frame(fr_product_bottom, height=80)
    fr_product_bottom_2.pack(side=TOP, anchor=NW)
    # fr_product_bottom_2.pack_propagate(0)

    # fr_input_sep_3 = Frame(fr_product_bottom, width=2, borderwidth=1, relief="groove")
    # fr_input_sep_3.pack(side=LEFT, fill=Y, padx=3, pady=2)

    fr_product_bottom_3 = Frame(fr_product_bottom)
    fr_product_bottom_3.pack(fill=BOTH, expand=True)
    fr_product_bottom_3.pack_propagate(0)

    fr_cover(fr_product_bottom_1)
    fr_product(fr_product_bottom_2)
    # fr_log(fr_product_bottom_3)

    pass


def init_fr_product():
    fr_product: Frame = global_widgets["fr_product"]
    fr_product_top = Frame(fr_product)
    fr_product_top_1 = Frame(fr_product)
    fr_product_bottom = Frame(fr_product)
    global_widgets["fr_product_top"] = fr_product_top
    global_widgets["fr_product_bottom"] = fr_product_bottom

    fr_product_top.pack(side=TOP, fill=X)
    fr_product_top_1.pack(side=TOP, fill=X)
    fr_product_bottom.pack(fill=BOTH, expand=True)

    fr_top(fr_product_top, fr_product_top_1)
    fr_bottom(fr_product_bottom)

    pass


if __name__ == "__main__":
    pass
