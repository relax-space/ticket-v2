from tkinter import Tk


def center_window(root: Tk, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = int((ws / 2) - (w / 2))
    y = int((hs / 2) - (h / 2))
    root.geometry(f"{w}x{h}+{x}+{y}")
