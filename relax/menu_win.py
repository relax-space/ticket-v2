import copy
from tkinter import (
    BOTH,
    END,
    LEFT,
    RIGHT,
    X,
    Y,
    Button,
    Entry,
    Event,
    EventType,
    Frame,
    Label,
    Listbox,
    Menu,
    Scrollbar,
    Toplevel,
    messagebox,
)
from relax.product_win_data import render_product_data
from relax.ticket_win_data import render_ticket_data
from relax.top_win_data import render_top_data
from relax.util_win import center_window
from PIL import Image, ImageTk
import tkinter.font as tkFont
from relax.util import (
    global_widgets,
    global_raw_data,
    delete_current_data,
    get_current_data,
    get_template_data,
    update_current_data,
    update_raw_data,
)
from relax.win_data import render_data


def show_top(tip, default_content, on_event):
    root = global_widgets["root"]
    popup = Toplevel(root)
    popup.title(tip)
    center_window(popup, 200, 100)
    popup.resizable(False, False)
    lbl_msg = Label(popup, text="", fg="red")
    lbl_msg.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0))

    ety = Entry(popup)
    ety.insert(0, default_content)
    ety.focus_set()
    ety.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10))

    def exist_item(name):
        lst_menu: Listbox = global_widgets["lst_menu"]
        menu_list = lst_menu.get(0, END)
        for v in menu_list:
            if v == name:
                return True
        return False

    def comfirm(on_event):
        new_name = ety.get()
        if not new_name:
            messagebox.showinfo("提示", "不能为空")
            return
        is_has = exist_item(new_name)
        if is_has:
            lbl_msg.config(text="存在同样名字的模板")
            return
        on_event(new_name)
        popup.destroy()

    btn1 = Button(popup, text="确定", command=lambda: comfirm(on_event))
    btn1.grid(row=2, column=0, padx=(20, 0), pady=(0, 10), ipadx=10)
    btn2 = Button(popup, text="取消", command=popup.destroy)
    btn2.grid(row=2, column=1, padx=(0, 20), pady=(0, 10), ipadx=10)


def on_default(lst_menu: Listbox):
    indexs = lst_menu.curselection()
    if not indexs:
        messagebox.showinfo("警告", "请先选择要设置默认的模板")
        return
    index = indexs[0]
    key = lst_menu.get(index)

    current_data_index = 0
    for i, v in enumerate(global_raw_data):
        v["checked"] = False
        if v["menu_name"] == key:
            current_data_index = i
    current_data = global_raw_data.pop(current_data_index)
    current_data["checked"] = True
    global_raw_data.insert(0, current_data)

    lst_menu.delete(0, END)
    for i in global_raw_data:
        lst_menu.insert(END, i["menu_name"])
    lst_menu.select_set(0)

    update_raw_data()
    pass


def on_add(lst_menu: Listbox):
    def on_event(new_name):
        lst_menu.insert(END, new_name)
        lst_menu.select_clear(0, END)
        lst_menu.select_set(END)

        t_data = copy.deepcopy(get_template_data())
        t_data["menu_name"] = new_name
        render_data(t_data)
        global_raw_data.append(t_data)
        update_raw_data()
        pass

    show_top("新增", "", on_event)
    pass


def on_edit(lst_menu: Listbox):
    indexs = lst_menu.curselection()
    if not indexs:
        messagebox.showinfo("警告", "请先选择要编辑的模板")
        return
    index = indexs[0]
    default_content = lst_menu.get(index)

    def on_event(new_name):
        update_current_data(default_content, new_name)
        update_raw_data()

        lst_menu.delete(index)
        lst_menu.insert(index, new_name)
        lst_menu.select_set(index)
        pass

    show_top("编辑", default_content, on_event)


def on_delete(lst_menu: Listbox):
    indexs = lst_menu.curselection()
    if not indexs:
        messagebox.showinfo("警告", "请先选择要删除的模板！")
        return
    menu_list: list = lst_menu.get(0, END)
    if len(menu_list) == 1:
        messagebox.showinfo("警告", "最后一个模板，禁止删除！")
        return

    result = messagebox.askquestion("提示", "您确定要删除吗？")
    if result != "yes":
        return
    index = indexs[0]
    key = lst_menu.get(index)
    lst_menu.delete(index)
    delete_current_data(key)
    update_raw_data()

    new_key = lst_menu.get(0)
    current_data = get_current_data(new_key)
    render_data(current_data)
    lst_menu.select_set(0)
    pass


def init_top(fr_1: Frame, lst_menu):
    lbl_1 = Label(fr_1, text="模板")
    lbl_1.pack(fill=X, side=LEFT)

    img_path_list = [
        "asset/trash.png",
        "asset/edit.png",
        "asset/new.png",
    ]

    def get_command(name, lst_menu):
        match name:
            case "asset/new.png":
                return lambda: on_add(lst_menu)
            case "asset/edit.png":
                return lambda: on_edit(lst_menu)
            case "asset/trash.png":
                return lambda: on_delete(lst_menu)

    for i in img_path_list:
        img1 = Image.open(i)
        img1 = img1.resize((20, 20))
        img1 = ImageTk.PhotoImage(img1)
        event = get_command(i, lst_menu)
        btn1 = Button(
            fr_1,
            image=img1,
            borderwidth=0,
            command=event,
        )
        btn1.pack(fill=X, side=RIGHT, pady=0)
        btn1.image = img1
    pass


def init_bottom(fr_1: Frame) -> Listbox:
    sb_menu = Scrollbar(fr_1)
    lst_menu = Listbox(fr_1, exportselection=False, yscrollcommand=sb_menu.set)
    sb_menu.config(command=lst_menu.yview)

    def left_click(e: Event):
        indexs = lst_menu.curselection()
        if not indexs:
            return
        key = lst_menu.get(indexs[0])
        current_data = get_current_data(key)
        render_data(current_data)
        pass

    def right_click(e: Event):
        index = lst_menu.nearest(e.y)
        if index == -1:
            return
        lst_menu.select_clear(0, END)
        lst_menu.select_set(index)

        key = lst_menu.get(index)
        current_data = get_current_data(key)
        render_data(current_data)

        right_click_menu.post(e.x_root, e.y_root)
        pass

    lst_menu.bind("<<ListboxSelect>>", left_click)
    lst_menu.bind("<Button-3>", right_click)

    right_click_menu = Menu(fr_1, tearoff=0)
    right_click_menu.add_command(label="设置为默认", command=lambda: on_default(lst_menu))
    right_click_menu.add_command(label="添加", command=lambda: on_add(lst_menu))
    right_click_menu.add_command(label="重命名", command=lambda: on_edit(lst_menu))
    right_click_menu.add_command(label="删除", command=lambda: on_delete(lst_menu))

    sb_menu.pack(side=RIGHT, fill=Y)
    lst_menu.pack(fill=BOTH, expand=True)

    global_widgets["lst_menu"] = lst_menu
    return lst_menu

    pass


def init_fr_menu():
    fr_menu = global_widgets["fr_menu"]
    fr_1 = Frame(fr_menu)
    fr_1.pack(fill=X)

    fr_2 = Frame(fr_menu)
    fr_2.pack(fill=BOTH, expand=True)

    lst_menu = init_bottom(fr_2)
    init_top(fr_1, lst_menu)
    pass
