"""
商品清单
"""
from tkinter.font import Font
from util import _widgets
from tkinter import (
    BOTH,
    BOTTOM,
    E,
    END,
    LEFT,
    NW,
    RIGHT,
    TOP,
    VERTICAL,
    W,
    X,
    Y,
    Button,
    Checkbutton,
    Entry,
    Frame,
    Label,
    Scrollbar,
    Text,
    Tk,
)


def fr_top(fr_product_top):
    lbl_product_input = Label(fr_product_top, text="商品输入路径：")
    ety_product_input = Entry(fr_product_top, width=60)
    btn_product_input = Button(fr_product_top, text="选择")

    btn_product_create = Button(fr_product_top, text="生成", width=15)

    lbl_cover_1 = Label(fr_product_top, text="封面标题1：")
    ety_cover_1 = Entry(fr_product_top, width=60)
    lbl_cover_2 = Label(fr_product_top, text="封面标题2：")
    ety_cover_2 = Entry(fr_product_top, width=60)

    lbl_product_output = Label(fr_product_top, text="商品输出路径：")
    ety_product_output = Entry(fr_product_top, width=60)
    btn_product_output = Button(fr_product_top, text="选择")

    chk_import = Checkbutton(fr_product_top, text="是否批量生成导入列表：")
    lbl_remark_1 = Label(fr_product_top, text="(如果不需要，下面的不用设置)")
    lbl_import = Label(fr_product_top, text="税率表：")
    ety_import = Entry(fr_product_top, width=60)
    btn_import = Button(fr_product_top, text="选择")

    chk_page_size = Checkbutton(fr_product_top, text="是否批量设置页面尺寸：")
    lbl_remark_2 = Label(fr_product_top, text="(如果不需要，下面的不用设置)")
    lbl_page_size = Label(fr_product_top, text="尺寸表：")
    ety_page_size = Entry(fr_product_top, width=60)
    btn_page_size = Button(fr_product_top, text="选择")

    row_index = 0
    lbl_product_input.grid(row=row_index, column=0, sticky=E, pady=(10, 3))
    ety_product_input.grid(row=row_index, column=1, pady=(10, 3))
    btn_product_input.grid(row=row_index, column=2, pady=(10, 3))

    btn_product_create.grid(
        row=row_index,
        column=3,
        rowspan=4,
        padx=(40, 0),
        pady=(20, 20),
        sticky="W" + "E" + "N" + "S",
    )

    row_index += 1
    lbl_cover_1.grid(row=row_index, column=0, sticky=E, pady=(0, 8))
    ety_cover_1.grid(row=row_index, column=1, pady=(0, 8))

    row_index += 1
    lbl_cover_2.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_cover_2.grid(row=row_index, column=1, pady=(0, 3))

    row_index += 1
    lbl_product_output.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_product_output.grid(row=row_index, column=1, pady=(0, 3))
    btn_product_output.grid(row=row_index, column=2, pady=(0, 3))

    row_index += 1
    chk_import.grid(row=row_index, column=0, pady=(0, 3))
    lbl_remark_1.grid(row=row_index, column=1, sticky="w")

    row_index += 1
    lbl_import.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_import.grid(row=row_index, column=1, pady=(0, 3))
    btn_import.grid(row=row_index, column=2, pady=(0, 3))

    row_index += 1
    chk_page_size.grid(row=row_index, column=0, pady=(0, 3))
    lbl_remark_2.grid(row=row_index, column=1, sticky="w")
    row_index += 1
    lbl_page_size.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_page_size.grid(row=row_index, column=1, pady=(0, 3))
    btn_page_size.grid(row=row_index, column=2, pady=(0, 3))

    _widgets["ety_product_input"] = ety_product_input
    _widgets["btn_product_input"] = btn_product_input
    _widgets["ety_cover_1"] = ety_cover_1
    _widgets["ety_cover_2"] = ety_cover_2
    _widgets["ety_product_output"] = ety_product_output
    _widgets["chk_import"] = chk_import
    _widgets["ety_import"] = ety_import
    _widgets["btn_import"] = btn_import
    _widgets["chk_page_size"] = chk_page_size
    _widgets["ety_page_size"] = ety_page_size
    _widgets["btn_page_size"] = btn_page_size
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
        _widgets[f"lbl_column_width_cover_{i}"] = lbl_column_width
        _widgets[f"ety_column_width_cover_{i}"] = ety_column_width

    column_index = 0
    lbl_column_width_title.grid(row=0, column=column_index, sticky=E, padx=(48, 0))
    column_index += 1
    for v in list:
        lbl_column_width: Label = _widgets[f"lbl_column_width_cover_{v}"]
        ety_column_width: Entry = _widgets[f"ety_column_width_cover_{v}"]
        lbl_column_width.grid(row=0, column=column_index, sticky=E, padx=(0, 10))
        column_index += 1
        ety_column_width.grid(row=0, column=column_index)
        column_index += 1

    fr_2.pack(side=TOP, anchor=NW)

    fr_3 = Frame(fr_product_bottom_1)

    lbl_row_1 = Label(fr_3, text="第一行，行高：")
    ety_row_1 = Entry(fr_3, width=3, justify=RIGHT)
    lbl_content_1 = Label(fr_3, text="内容：")
    ety_content_1 = Entry(fr_3, width=60)

    lbl_row_2 = Label(fr_3, text="第二行，行高：")
    ety_row_2 = Entry(fr_3, width=3, justify=RIGHT)
    lbl_content_2 = Label(fr_3, text="内容：")
    ety_content_2 = Entry(fr_3, width=60)

    lbl_row_3 = Label(fr_3, text="第三行，行高：")
    ety_row_3 = Entry(fr_3, width=3, justify=RIGHT)
    lbl_content_3 = Label(fr_3, text="内容：")
    ety_content_3 = Entry(fr_3, width=60)

    lbl_row_4 = Label(fr_3, text="数据行，行高：")
    ety_row_4 = Entry(fr_3, width=3, justify=RIGHT)
    lbl_content_4 = Label(fr_3, text="内容：")
    ety_content_4 = Entry(fr_3, width=60)

    lbl_row_5 = Label(fr_3, text="汇总行，行高：")
    ety_row_5 = Entry(fr_3, width=3, justify=RIGHT)
    lbl_content_5 = Label(fr_3, text="内容：")
    ety_content_5 = Entry(fr_3, width=60)

    lbl_row_6 = Label(fr_3, text="盖章行，行高：")
    ety_row_6 = Entry(fr_3, width=3, justify=RIGHT)
    lbl_content_6 = Label(fr_3, text="内容：")
    ety_content_6 = Entry(fr_3, width=60)

    row_index = 0
    lbl_row_1.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_row_1.grid(row=row_index, column=1)
    lbl_content_1.grid(row=row_index, column=2)
    ety_content_1.grid(row=row_index, column=3)
    row_index += 1
    lbl_row_2.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_row_2.grid(row=row_index, column=1)
    lbl_content_2.grid(row=row_index, column=2)
    ety_content_2.grid(row=row_index, column=3)
    row_index += 1
    lbl_row_3.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_row_3.grid(row=row_index, column=1)
    lbl_content_3.grid(row=row_index, column=2)
    ety_content_3.grid(row=row_index, column=3)
    row_index += 1
    lbl_row_4.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_row_4.grid(row=row_index, column=1)
    lbl_content_4.grid(row=row_index, column=2)
    ety_content_4.grid(row=row_index, column=3)
    row_index += 1
    lbl_row_5.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_row_5.grid(row=row_index, column=1)
    lbl_content_5.grid(row=row_index, column=2)
    ety_content_5.grid(row=row_index, column=3)
    row_index += 1
    lbl_row_6.grid(row=row_index, column=0, sticky=E, pady=(0, 3))
    ety_row_6.grid(row=row_index, column=1)
    lbl_content_6.grid(row=row_index, column=2)
    ety_content_6.grid(row=row_index, column=3)

    fr_3.pack(fill=BOTH, pady=(3, 0))
    pass


def fr_product(fr_product_bottom_2):
    fr_1 = Frame(fr_product_bottom_2, height=25)
    fr_2 = Frame(fr_product_bottom_2)

    lbl_1 = Label(fr_1, text="商品设置")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))

    lbl_1.pack(side=TOP)
    fr_1.pack(side=TOP, anchor=NW)
    fr_2.pack(fill=BOTH)
    pass


def fr_log(fr_product_bottom_3):
    fr_1 = Frame(fr_product_bottom_3, height=20)
    fr_2 = Frame(fr_product_bottom_3)
    lbl_1 = Label(fr_1, text="执行日志")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))
    txt_content = Text(fr_2)
    slb = Scrollbar(orient=VERTICAL, command=txt_content.yview)
    txt_content.configure(yscrollcommand=slb.set, state="disabled")

    lbl_1.pack(side=LEFT, fill=X)
    txt_content.pack(fill=BOTH, expand=True, padx=10, pady=(3, 0))
    fr_1.pack(side=TOP, fill=X)
    fr_2.pack(fill=BOTH, expand=True)
    pass


def fr_bottom(fr_product_bottom: Frame):
    fr_input_sep_1 = Frame(fr_product_bottom, height=2, borderwidth=1, relief="groove")
    fr_input_sep_1.pack(side=TOP, fill=X, padx=3, pady=5)

    fr_product_bottom_1 = Frame(fr_product_bottom, width=600)
    fr_product_bottom_1.pack(side=LEFT, fill=Y)
    fr_product_bottom_1.pack_propagate(0)

    # fr_input_sep_2 = Frame(fr_product_bottom, width=2, borderwidth=1, relief="groove")
    # fr_input_sep_2.pack(side=LEFT, fill=Y, padx=3, pady=2)

    # fr_product_bottom_2 = Frame(fr_product_bottom, width=440)
    # fr_product_bottom_2.pack(side=LEFT, fill=Y)
    # fr_product_bottom_2.pack_propagate(0)

    # fr_input_sep_3 = Frame(fr_product_bottom, width=2, borderwidth=1, relief="groove")
    # fr_input_sep_3.pack(side=LEFT, fill=Y, padx=3, pady=2)

    # fr_product_bottom_3 = Frame(fr_product_bottom)
    # fr_product_bottom_3.pack(fill=BOTH, expand=True)
    # fr_product_bottom_3.pack_propagate(0)

    fr_cover(fr_product_bottom_1)
    # fr_product(fr_product_bottom_2)
    # fr_log(fr_product_bottom_3)

    pass


def init_fr_product():
    fr_product: Frame = _widgets["fr_product"]
    fr_product_top = Frame(fr_product)
    fr_product_bottom = Frame(fr_product)
    _widgets["fr_product_top"] = fr_product_top
    _widgets["fr_product_bottom"] = fr_product_bottom

    fr_product_top.pack(side=TOP, fill=X)
    fr_product_bottom.pack(fill=BOTH, expand=True)

    fr_top(fr_product_top)
    fr_bottom(fr_product_bottom)

    pass


if __name__ == "__main__":
    pass
