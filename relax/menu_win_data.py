from tkinter import END, Listbox
from relax.util_win import _widgets


def render_menu_data(current_menu_index: int, menu_list: list):
    lst_menu: Listbox = _widgets["lst_menu"]
    for i in menu_list:
        lst_menu.insert(END, i)
    lst_menu.select_set(current_menu_index)
    pass
