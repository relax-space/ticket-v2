from tkinter import (
    BOTH,
    GROOVE,
    LEFT,
    TOP,
    X,
    Y,
    BooleanVar,
    Frame,
    StringVar,
    Tk,
    Button,
    DISABLED,
    NORMAL,
    PhotoImage,
)
from tkinter.ttk import Notebook
from relax.menu_win_data import render_menu_data
from relax.product_win import init_fr_product
from relax.product_win_data import render_product_data
from relax.ticket_win import init_fr_ticket
from relax.menu_win import init_fr_menu
from relax.ticket_win_data import render_ticket_data
from relax.top_win import init_fr_top
from relax.top_win_data import render_top_data
from relax.util import (
    init_const,
    init_raw_data,
    global_widgets,
    global_dict_chk_var,
    global_raw_data,
    global_config_data,
)
from relax.util_win import center_window
from os import path as os_path, makedirs
from relax.secret_win import init_secret, get_check_result, show_active_btn


def init_view(root):
    fr_menu = Frame(root, width=180, relief=GROOVE, bd=1)
    fr_menu.pack(side=LEFT, fill=Y)
    fr_menu.pack_propagate(0)
    fr_top = Frame(root, height=25)
    fr_top.pack(padx=10, pady=(5, 0), side=TOP, fill=X)
    fr_top_1 = Frame(root, height=10)
    fr_top_1.pack(padx=104, pady=(0, 10), side=TOP, fill=X)

    fr_input_sep_1 = Frame(root, height=2, borderwidth=1, relief="groove")
    fr_input_sep_1.pack(side=TOP, fill=X, padx=3, pady=2)

    ndb = Notebook(root)
    fr_product = Frame()
    fr_ticket = Frame()
    ndb.add(fr_product, text="商品清单")
    ndb.add(fr_ticket, text="发票清单")
    ndb.pack(pady=1, expand=True, fill=BOTH)

    global_widgets["root"] = root
    global_widgets["fr_menu"] = fr_menu
    global_widgets["fr_top"] = fr_top
    global_widgets["fr_top_1"] = fr_top_1
    global_widgets["ndb"] = ndb
    global_widgets["fr_product"] = fr_product
    global_widgets["fr_ticket"] = fr_ticket

    init_fr_menu()
    init_fr_top()
    init_fr_product()
    init_fr_ticket()


def init_perm():
    result = get_check_result()
    show_active_btn(result[0])


def init_data():
    init_raw_data()
    current_data = {}
    current_menu_index = 0
    menu_list = []
    for i, v in enumerate(global_raw_data):
        if v["checked"]:
            current_data = v
            current_menu_index = i
        menu_list.append(v["menu_name"])
        pass
    render_top_data(current_data)
    render_menu_data(current_menu_index, menu_list)
    render_product_data(current_data)
    render_ticket_data(current_data)
    pass


def create_folder():
    if not os_path.isdir("data"):
        makedirs("data")
    temp = "temp"
    if not os_path.isdir(temp):
        makedirs(temp)
    p1 = os_path.join(temp, "cover")
    p2 = os_path.join(temp, "product")
    if not os_path.isdir(p1):
        makedirs(p1)
    if not os_path.isdir(p2):
        makedirs(p2)
    pass


def main_win_start():
    create_folder()

    root = Tk()
    root.title("发票清单-部队 V1.4")

    center_window(root, 1024, 768)
    global_widgets["root"] = root
    global_dict_chk_var["_import_var"] = BooleanVar()
    global_dict_chk_var["_page_size_var"] = BooleanVar()
    global_dict_chk_var["_stamp_var"] = BooleanVar()
    global_dict_chk_var["_merge_same_product_var"] = BooleanVar()
    global_dict_chk_var["_import_var_option"] = StringVar()

    init_const()
    global_config_data["is_actived"] = False
    if not init_secret():
        return

    init_view(root)
    init_data()
    init_perm()
    root.mainloop()
    pass


if __name__ == "__main__":
    main_win_start()
    pass
