from tkinter import BOTH, E, RIGHT, TOP, X, Button, Entry, Frame, Label, Tk
from tkinter.ttk import Combobox, Notebook
from product_win import init_fr_product
from ticket_win import init_fr_ticket
from util import _widgets
from util_win import center_window


def init_fr_top():
    fr_top: Frame = _widgets["fr_top"]
    lbl_1 = Label(fr_top, text="模板：")
    cbo_master = Combobox(fr_top, width=40)
    btn_master = Button(fr_top, text="保存为模板")
    btn_master_edit = Button(fr_top, text="编辑模板")

    btn_master_edit.pack(side=RIGHT, padx=(3, 10))
    btn_master.pack(side=RIGHT, padx=(3, 0))
    cbo_master.pack(side=RIGHT, padx=(3, 0))
    lbl_1.pack(side=RIGHT, padx=(3, 0))
    pass


def main():
    root = Tk()
    root.title("发票清单-部队")
    center_window(root, 1024, 768)
    fr_top = Frame(root, height=25)
    fr_top.pack(padx=10, pady=5, side=TOP, fill=X)

    ndb = Notebook(root)
    fr_product = Frame()
    fr_ticket = Frame()
    ndb.add(fr_product, text="商品清单")
    ndb.add(fr_ticket, text="发票清单")
    ndb.pack(padx=10, pady=5, expand=True, fill=BOTH)

    _widgets["root"] = root
    _widgets["fr_top"] = fr_top
    _widgets["ndb"] = ndb
    _widgets["fr_product"] = fr_product
    _widgets["fr_ticket"] = fr_ticket

    init_fr_top()
    init_fr_product()
    init_fr_ticket()

    root.mainloop()
    pass


if __name__ == "__main__":
    main()
    pass
