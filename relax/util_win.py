from tkinter import END, Text, Tk
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
