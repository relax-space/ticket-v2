from tkinter import DISABLED, END, W, Entry, Label, Text, Tk, Toplevel
from relax.util import global_widgets
from tkinter import Button
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip


def center_window(root: Tk, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int((ws / 2) - (w / 2))
    y = int((hs / 2) - (h / 2))
    root.geometry(f"{w}x{h}+{x}+{y}")


def log_product(content: str):
    txt_product_log: Text = global_widgets["txt_product_log"]
    txt_product_log.configure(state="normal")
    txt_product_log.insert(END, f"{content}\n")
    txt_product_log.see(END)
    txt_product_log.configure(state="disabled")


def log_product_clear():
    txt_product_log: Text = global_widgets["txt_product_log"]
    txt_product_log.configure(state="normal")
    txt_product_log.delete("1.0", END)
    txt_product_log.configure(state="disabled")


def render_tooltip(fr, path: str, content: str, rect: tuple):
    # (20, 20)
    img1 = Image.open(path)
    img1 = img1.resize(rect)
    img1 = ImageTk.PhotoImage(img1)
    btn1 = Button(fr, image=img1, borderwidth=0)
    Hovertip(btn1, content, hover_delay=1)
    return btn1, img1


def show_Toplevel(title: str, zd_list_str: str):
    root = global_widgets["root"]
    popup = Toplevel(root)
    popup.title("警告")
    center_window(popup, 700, 300)
    lbl_msg = Label(
        popup,
        text=title,
    )
    txt_content = Text(
        popup,
        width=120,
        relief="flat",
        bg="gray94",
        wrap="word",
    )
    txt_content.insert(1.0, zd_list_str)
    txt_content.config(state=DISABLED)

    lbl_msg.grid(row=0, column=0, sticky=W, pady=(5, 0))
    txt_content.grid(row=1, column=0, sticky=W)
