from tkinter import (
    E,
    END,
    RIGHT,
    W,
    Button,
    Checkbutton,
    Entry,
    Frame,
    Label,
    Listbox,
    filedialog,
    messagebox,
)
from relax.util import (
    get_current_data,
    update_raw_data,
    global_widgets,
    global_dict_chk_var,
)
from relax.win_data import json_data
from relax.util_win import render_tooltip
from PIL import Image, ImageTk


def save_template():
    lst_menu = global_widgets["lst_menu"]
    indexs = lst_menu.curselection()
    if not indexs:
        messagebox.showinfo("警告", "请先在左边选择一个模板！")
        return
    index = indexs[0]
    key = lst_menu.get(index)
    current_data = get_current_data(key)

    json_data(current_data)
    update_raw_data()
    messagebox.showinfo("提示", "保存成功!")
    pass


def set_output_folder():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    ety_output_path: Entry = global_widgets["ety_output_path"]
    ety_output_path.delete(0, END)
    ety_output_path.insert(0, folder_path)
    pass


def page_size_click():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    ety_page_size: Entry = global_widgets["ety_page_size"]
    ety_page_size.delete(0, END)
    ety_page_size.insert(0, file_path)
    pass


def init_fr_top():
    fr_top: Frame = global_widgets["fr_top"]
    btn_master_edit = Button(fr_top, text="保存为模板", command=save_template)
    lbl_supplier_name = Label(fr_top, text="供应商名称：*", fg="red")
    ety_supplier_name = Entry(fr_top, width=60)

    lbl_output_path = Label(fr_top, text="输出文件夹路径：")
    ety_output_path = Entry(fr_top, width=60)
    btn_output_path = Button(fr_top, text="选择", command=set_output_folder)

    chk_page_size = Checkbutton(
        fr_top, text="是否批量设置页面尺寸：", variable=global_dict_chk_var["_page_size_var"]
    )
    lbl_remark_2 = Label(fr_top, text="(如果不勾选，下面的设置不会生效)")

    fr_0 = Frame(fr_top)
    lbl_page_size = Label(fr_0, text="尺寸表:")
    btn1, img1 = render_tooltip(
        fr_0, "asset/question.png", "只会读取excel的第一个sheet！", (15, 15)
    )
    ety_page_size = Entry(fr_0, width=60)
    btn_page_size = Button(fr_0, text="选择", command=page_size_click)

    lbl_page_size.grid(row=0, column=0, sticky=E, padx=(52, 0))
    btn1.grid(row=0, column=1)
    btn1.image = img1
    ety_page_size.grid(row=0, column=2, padx=(10, 0))
    btn_page_size.grid(row=0, column=3)

    row_index = 0
    btn_master_edit.grid(row=row_index, column=0)

    row_index += 1
    lbl_supplier_name.grid(row=row_index, column=0, pady=(2, 0), sticky=E)
    ety_supplier_name.grid(row=row_index, column=1)

    row_index += 1
    lbl_output_path.grid(row=row_index, column=0, pady=(2, 0), sticky=E)
    ety_output_path.grid(row=row_index, column=1, sticky=W)
    btn_output_path.grid(row=row_index, column=2)

    row_index += 1
    chk_page_size.grid(row=row_index, column=0, pady=(2, 0), sticky=E)
    lbl_remark_2.grid(row=row_index, column=1, sticky=W)
    row_index += 1
    fr_0.grid(row=row_index, column=0, columnspan=4, padx=(36, 0), sticky=W)

    # lbl_page_size.grid(row=row_index, column=0, pady=(3, 0), sticky=E)
    # btn1.grid(row=row_index, column=1, pady=(3, 0), sticky=W)
    # btn1.image = img1
    # ety_page_size.grid(row=row_index, column=2, pady=(3, 0), sticky=W)
    # btn_page_size.grid(row=row_index, column=3, pady=(3, 0), sticky=W)

    global_widgets["ety_supplier_name"] = ety_supplier_name
    global_widgets["ety_output_path"] = ety_output_path

    global_widgets["chk_page_size"] = chk_page_size
    global_widgets["ety_page_size"] = ety_page_size
    global_widgets["btn_page_size"] = btn_page_size

    fr_top_1 = global_widgets["fr_top_1"]
    lbl_page_height = Label(fr_top_1, text="页面高度：")
    lbl_A4_page_height = Label(fr_top_1, text="A4：")
    ety_A4_page_height = Entry(fr_top_1, width=6, justify=RIGHT)
    lbl_A5_page_height = Label(fr_top_1, text="A5：")
    ety_A5_page_height = Entry(fr_top_1, width=6, justify=RIGHT)

    row_index = 0
    lbl_page_height.grid(row=row_index, column=0, pady=(3, 0), sticky=E)
    lbl_A4_page_height.grid(row=row_index, column=1, pady=(3, 0), sticky=W)
    ety_A4_page_height.grid(row=row_index, column=2, pady=(3, 0), sticky=W)
    lbl_A5_page_height.grid(
        row=row_index, column=3, padx=(10, 0), pady=(3, 0), sticky=W
    )
    ety_A5_page_height.grid(row=row_index, column=4, pady=(3, 0), sticky=W)

    global_widgets["ety_A4_page_height"] = ety_A4_page_height
    global_widgets["ety_A5_page_height"] = ety_A5_page_height
    pass
