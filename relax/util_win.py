from tkinter import END, Text, Tk, BooleanVar

_widgets = {}
_dict_chk_var = {"_import_var": "", "_page_size_var": "", "_stamp_var": ""}


def center_window(root: Tk, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int((ws / 2) - (w / 2))
    y = int((hs / 2) - (h / 2))
    root.geometry(f"{w}x{h}+{x}+{y}")


def log_product(content: str):
    txt_product_log: Text = _widgets["txt_product_log"]
    txt_product_log.configure(state="normal")
    txt_product_log.insert(END, f"{content}\n")
    txt_product_log.see(END)
    txt_product_log.configure(state="disabled")


def log_product_clear():
    txt_product_log: Text = _widgets["txt_product_log"]
    txt_product_log.configure(state="normal")
    txt_product_log.delete("1.0", END)
    txt_product_log.configure(state="disabled")
