"""
发票
"""
from shutil import rmtree
from tkinter import (
    E,
    END,
    NW,
    TOP,
    X,
    Button,
    Entry,
    Frame,
    Label,
    Listbox,
    filedialog,
    messagebox,
)
from tkinter.font import Font
from traceback import format_exc
from relax.ticket_print import make_ticket_file

from relax.util import (
    fill_zero_2,
    get_current_data,
    global_widgets,
    global_dict_chk_var,
    global_config_data,
)
from relax.win_data import json_data
from os import makedirs, path as os_path, startfile as os_startfile
from relax.read_excel_file import (
    read_one_ticket,
    get_ticket_mapping,
    get_page_size_list,
)


def ticket_folder_click():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return
    ety_ticket_folder: Entry = global_widgets["ety_ticket_folder"]
    ety_ticket_folder.delete(0, END)
    ety_ticket_folder.insert(0, folder_path)
    pass


def ticket_mapping_click():
    lst_menu: Listbox = global_widgets["lst_menu"]
    if not lst_menu.curselection():
        messagebox.showinfo("提示", "请先在左边选择一个模板")
        return
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    ety_ticket_mapping: Entry = global_widgets["ety_ticket_mapping"]
    ety_ticket_mapping.delete(0, END)
    ety_ticket_mapping.insert(0, file_path)
    pass


def create_click_valid():
    lst_menu: Listbox = global_widgets["lst_menu"]
    ety_supplier_name: Entry = global_widgets["ety_supplier_name"]
    ety_output_path: Entry = global_widgets["ety_output_path"]
    ety_page_size: Entry = global_widgets["ety_page_size"]
    ety_A4_page_height: Entry = global_widgets["ety_A4_page_height"]
    ety_A5_page_height: Entry = global_widgets["ety_A5_page_height"]

    ety_ticket_folder: Entry = global_widgets["ety_ticket_folder"]
    ety_ticket_mapping: Entry = global_widgets["ety_ticket_mapping"]
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
    elif global_dict_chk_var["_page_size_var"]:
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
    elif not ety_ticket_folder.get():
        messagebox.showwarning("警告", "发票文件夹不能为空！")
        ety_ticket_folder.focus_get()
        return False
    elif not ety_ticket_mapping.get():
        messagebox.showwarning("警告", "发票映射文件（xlsx）不能为空！")
        ety_ticket_mapping.focus_get()
        return False
    return True


def ticket_create_click_raw(only_zd_list):
    if not create_click_valid():
        return
    lst_menu: Listbox = global_widgets["lst_menu"]
    ety_supplier_name: Entry = global_widgets["ety_supplier_name"]
    ety_ticket_folder: Entry = global_widgets["ety_ticket_folder"]
    ety_ticket_mapping: Entry = global_widgets["ety_ticket_mapping"]

    key = lst_menu.get(lst_menu.curselection()[0])
    current_data = get_current_data(key)
    json_data(current_data)
    ticket_folder_path = ety_ticket_folder.get()
    ticket_mapping_path = ety_ticket_mapping.get()

    ticket_data = current_data["ticket"]
    year, month, supplier = read_one_ticket(ticket_mapping_path, ticket_data)
    supplier_name = ety_supplier_name.get()
    if supplier != supplier_name:
        messagebox.showwarning(
            "警告",
            "供应商名字不一致：文件中和界面上的供应商名字不一致，请确认!",
        )
        ety_supplier_name.focus()
        return
    output_folder_path = os_path.join(
        current_data["output_path"], supplier, f"{year}{fill_zero_2(month)}"
    )
    if not os_path.isdir(output_folder_path):
        makedirs(output_folder_path)

    zd_ticket_set, mapping_list = get_ticket_mapping(
        ticket_folder_path, ticket_mapping_path, ticket_data
    )
    if only_zd_list:
        new_mapping_list = []
        zd_ticket_set = set()
        for i in mapping_list:
            zd = i[1]
            if zd in only_zd_list:
                new_mapping_list.append(i)
                zd_ticket_set.add(zd)
        mapping_list = new_mapping_list
        pass
    batch_size = current_data["batch_size"]
    zd_size_set, product_size_dict, ticket_size_dict = get_page_size_list(
        batch_size, year, month
    )
    if zd_size_set:
        zd_diff = zd_ticket_set.difference(zd_size_set)
        if zd_diff:
            messagebox.showwarning("警告", f"尺寸表缺少灶点号：{zd_diff}")
            return

        def remove_unuse(unuse_set: set, size_dict):
            for i in unuse_set:
                del size_dict[i]
            pass

        unuse_set = zd_size_set.difference(zd_ticket_set)
        remove_unuse(unuse_set, product_size_dict)
        remove_unuse(unuse_set, ticket_size_dict)

    error_zd_list = make_ticket_file(
        ticket_folder_path,
        output_folder_path,
        mapping_list,
        ticket_size_dict,
        ticket_data,
    )

    ticket_source_path = os_path.join(
        output_folder_path, global_config_data["temp_ticket"]
    )
    if os_path.isdir(ticket_source_path):
        rmtree(ticket_source_path)
    if error_zd_list:
        messagebox.showwarning("批量导入提示", f"发票提示：以下灶点未成功，建议使用个别生成：{error_zd_list}")
    else:
        result = messagebox.askquestion("提示", "成功，你需要打开文件夹吗？")
        if result == "yes":
            os_startfile(output_folder_path)
    pass


def ticket_create_click():
    try:
        ticket_create_click_raw([])
    except Exception as e:
        messagebox.showerror("错误", format_exc())


def single_create():
    try:
        ety_ticket_zd_input: Entry = global_widgets["ety_ticket_zd_input"]
        zd_input_str = ety_ticket_zd_input.get()
        if not zd_input_str:
            messagebox.showwarning("警告", "灶点号不能为空！")
            ety_ticket_zd_input.focus_set()
            return
        if not create_click_valid():
            return
        zd_input_str = zd_input_str.replace("，", ",")
        only_zd_list: list = zd_input_str.split(",")
        ticket_create_click_raw(only_zd_list)
    except Exception as e:
        messagebox.showerror("错误", format_exc())
        pass


def fr_special_zd(fr_special: Frame):
    fr_1 = Frame(fr_special, height=25)

    lbl_1 = Label(fr_1, text="生成 - 个别灶点")
    font: dict[str, any] = Font(font=lbl_1["font"]).actual()
    lbl_1.configure(font=(font["family"], 10, "bold"))
    lbl_1.pack(side=TOP)
    fr_1.pack(side=TOP, anchor=NW, padx=(70, 0))

    fr_2 = Frame(fr_special)
    fr_2.pack(side=TOP, anchor=NW)
    lbl_zd_title = Label(fr_2, text=f"灶点号：")
    ety_ticket_zd_input = Entry(fr_2, width=60)
    btn_zd_input = Button(fr_2, text="个别生成", command=single_create)

    row_index = 0
    lbl_zd_title.grid(row=row_index, column=0, padx=(117, 0), sticky=E)
    ety_ticket_zd_input.grid(row=row_index, column=1, padx=(10, 0))
    btn_zd_input.grid(row=row_index, column=2)
    global_widgets["ety_ticket_zd_input"] = ety_ticket_zd_input
    pass


def init_fr_ticket():
    fr_ticket = global_widgets["fr_ticket"]
    fr_ticket_top = Frame(fr_ticket)
    fr_ticket_top.pack(side=TOP, fill=X)

    lbl_ticket_folder = Label(fr_ticket_top, text="发票文件夹：*", fg="red")
    ety_ticket_folder = Entry(fr_ticket_top, width=60)
    btn_ticket_folder = Button(fr_ticket_top, text="选择", command=ticket_folder_click)

    btn_ticket_create = Button(
        fr_ticket_top, text="生成", width=10, command=ticket_create_click
    )

    lbl_ticket_mapping = Label(fr_ticket_top, text="发票映射文件（xlsx）：*", fg="red")
    ety_ticket_mapping = Entry(fr_ticket_top, width=60)
    btn_ticket_mapping = Button(fr_ticket_top, text="选择", command=ticket_mapping_click)

    lbl_exclude_ticket_zd = Label(fr_ticket_top, text="排除灶点号：")
    ety_exclude_ticket_zd = Entry(fr_ticket_top, width=60)

    fr_special = Frame(fr_ticket_top)
    fr_special_zd(fr_special)

    row_index = 0
    lbl_ticket_folder.grid(
        row=row_index, column=0, sticky=E, padx=(20, 0), pady=(20, 0)
    )
    ety_ticket_folder.grid(row=row_index, column=1, pady=(20, 0))
    btn_ticket_folder.grid(row=row_index, column=2, pady=(20, 0))

    btn_ticket_create.grid(
        row=row_index,
        column=3,
        rowspan=2,
        padx=(40, 0),
        pady=(20, 0),
        sticky="WENS",
    )

    row_index += 1
    lbl_ticket_mapping.grid(
        row=row_index, column=0, sticky=E, padx=(20, 0), pady=(3, 0)
    )
    ety_ticket_mapping.grid(row=row_index, column=1, pady=(3, 0))
    btn_ticket_mapping.grid(row=row_index, column=2, pady=(3, 0))

    row_index += 1
    lbl_exclude_ticket_zd.grid(
        row=row_index, column=0, sticky=E, padx=(20, 0), pady=(3, 0)
    )
    ety_exclude_ticket_zd.grid(row=row_index, column=1, pady=(3, 0))

    row_index += 1
    fr_special.grid(row=row_index, column=0, columnspan=3)

    global_widgets["ety_ticket_folder"] = ety_ticket_folder
    global_widgets["ety_ticket_mapping"] = ety_ticket_mapping
    global_widgets["ety_exclude_ticket_zd"] = ety_exclude_ticket_zd

    pass


if __name__ == "__main__":
    pass
