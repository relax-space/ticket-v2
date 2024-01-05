from relax.util_request import get_current_date
from datetime import date
from relax.util import (
    check_date,
    check_file_date,
    global_check_result,
    update_const,
    global_config_data,
    global_widgets,
    global_dict_chk_var,
)
from b.secret_calc import SecretWin
from time import sleep
from tkinter import (
    Label,
    Entry,
    Button,
    font,
    Menu,
    StringVar,
    Toplevel,
    DISABLED,
    NORMAL,
    Frame,
)
from threading import Thread
from relax.util_win import center_window


def init_key():
    sw = SecretWin()
    code = global_config_data["code"]
    pwd = global_config_data["pwd"]
    th1 = Thread(target=sw.check_pwd, args=(global_check_result, code, pwd))
    th1.daemon = True
    th1.start()

    th2 = Thread(target=sw.get_code_thread, args=(global_check_result,))
    th2.daemon = True
    th2.start()

    th3 = Thread(target=check_date, args=(global_check_result,))
    th3.daemon = True
    th3.start()


def get_check_result(wait_seconds: int = 60):
    while wait_seconds > 0:
        if global_check_result[0] == "is_actived":
            wait_seconds -= 1
            sleep(1)
            continue
        else:
            global_config_data["is_actived"] = global_check_result[0]
            global_config_data["expired"] = global_check_result[1]
            break
    while wait_seconds > 0:
        if global_check_result[2] == "is_code":
            wait_seconds -= 1
            sleep(1)
            continue
        else:
            global_config_data["code"] = global_check_result[3]
            break
    while wait_seconds > 0:
        if global_check_result[4] == "today":
            wait_seconds -= 1
            sleep(1)
            continue
        else:
            break
    return global_check_result


def is_actived():
    if ("is_actived" not in global_config_data) or (
        not global_config_data["is_actived"]
    ):
        return False
    return True


def save_pwd():
    code: str = global_widgets["ety_code"].get().strip()
    pwd: str = global_widgets["ety_pwd"].get().strip()

    if (not pwd) or not pwd.strip():
        global_dict_chk_var["_error_msg_var"].set("激活码不能为空！")
        return
    elif len(pwd.strip()) != 32:
        global_dict_chk_var["_error_msg_var"].set("激活失败：激活码无效或已过期！")
        return
    is_enable, expired = SecretWin().check_pwd(global_check_result, code, pwd)
    if not is_enable:
        global_dict_chk_var["_error_msg_var"].set("激活失败：激活码无效或已过期！")
        return
    global_config_data["pwd"] = pwd
    global_config_data["expired"] = expired
    global_config_data["is_actived"] = True
    update_const()
    show_active_msg(True)
    show_active_btn(True)
    pass


def show_active_msg(success: bool):
    lbl_active_msg = global_widgets["lbl_active_msg"]
    if success:
        lbl_active_msg.config(fg="green")
        global_dict_chk_var["_active_msg_var"].set(
            f"已激活，有效期至：{global_config_data['expired']}"
        )
    else:
        lbl_active_msg.config(fg="red")
        global_dict_chk_var["_active_msg_var"].set(f"未激活或者已过期")


def show_active_btn(success: bool):
    btn_zd_input: Button = global_widgets["btn_zd_input"]
    btn_product_create: Button = global_widgets["btn_product_create"]
    btn_ticket_create: Button = global_widgets["btn_ticket_create"]
    btn_ticket_zd_input: Button = global_widgets["btn_ticket_zd_input"]
    if success:
        btn_zd_input.config(state=NORMAL)
        btn_product_create.config(state=NORMAL)
        btn_ticket_create.config(state=NORMAL)
        btn_ticket_zd_input.config(state=NORMAL)
    else:
        btn_zd_input.config(state=DISABLED)
        btn_product_create.config(state=DISABLED)
        btn_ticket_create.config(state=DISABLED)
        btn_ticket_zd_input.config(state=DISABLED)


def active_click(root):
    code_var = StringVar()
    pwd_var = StringVar()
    global_dict_chk_var["_active_msg_var"] = StringVar()
    global_dict_chk_var["_error_msg_var"] = StringVar()

    code_var.set(global_config_data["code"])
    pwd_var.set(global_config_data["pwd"])

    popup = Toplevel(root)
    popup.grab_set()
    popup.title("激活")
    popup.resizable(False, False)
    center_window(popup, 360, 180)

    lbl_active_msg = Label(popup, textvariable=global_dict_chk_var["_active_msg_var"])
    lbl_1 = Label(popup, text="机器码：")
    lbl_2 = Label(popup, text="激活码：")
    ety_code = Entry(popup, textvariable=code_var, width=40, state="readonly")
    ety_pwd = Entry(popup, textvariable=pwd_var, width=40)
    lbl_msg = Label(popup, textvariable=global_dict_chk_var["_error_msg_var"], fg="red")
    fr_1 = Frame(popup)
    btn_confirm = Button(fr_1, text="激活", command=save_pwd)
    btn_cancel = Button(fr_1, text="关闭", command=popup.destroy)
    btn_confirm.grid(
        row=0, column=0, ipadx=10, ipady=3, sticky="E", padx=(0, 40), pady=(0, 0)
    )
    btn_cancel.grid(row=0, column=1, ipadx=10, ipady=3, sticky="W", pady=(0, 0))

    lbl_active_msg.grid(row=0, column=1, columnspan=2, sticky="W", pady=(10, 0))

    lbl_1.grid(row=1, column=0, sticky="E", padx=(10, 0), pady=(3, 0))
    ety_code.grid(row=1, column=1, columnspan=2, padx=(3, 10), pady=(10, 0))
    lbl_2.grid(row=2, column=0, sticky="E", padx=(10, 0), pady=(10, 0))
    ety_pwd.grid(row=2, column=1, columnspan=2, padx=(3, 10), pady=(3, 0))

    lbl_msg.grid(row=3, column=1, columnspan=2, sticky="W")

    fr_1.grid(row=4, column=0, columnspan=3)

    global_widgets["lbl_active_msg"] = lbl_active_msg

    ety_pwd.focus_set()

    global_widgets["ety_code"] = ety_code
    global_widgets["ety_pwd"] = ety_pwd

    show_active_msg(is_actived())


def init_menu_activer():
    root = global_widgets["root"]
    menubar = Menu(root)
    activer = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=activer)
    activer.add_command(label="激活", command=lambda: active_click(root))
    root.config(menu=menubar)
    pass


def init_secret():
    init_key()
    init_menu_activer()
    return True
    pass
