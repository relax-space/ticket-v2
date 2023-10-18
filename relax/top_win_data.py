from tkinter import (
    END,
    Entry,
)

from relax.util_win import _widgets, _dict_chk_var


def render_top_data(current_data):
    ety_supplier_name: Entry = _widgets["ety_supplier_name"]
    ety_output_path: Entry = _widgets["ety_output_path"]
    ety_page_size: Entry = _widgets["ety_page_size"]
    ety_A4_page_height: Entry = _widgets["ety_A4_page_height"]
    ety_A5_page_height: Entry = _widgets["ety_A5_page_height"]

    ety_supplier_name.delete(0, END)
    ety_output_path.delete(0, END)
    ety_page_size.delete(0, END)
    ety_A4_page_height.delete(0, END)
    ety_A5_page_height.delete(0, END)

    ety_supplier_name.insert(END, current_data["supplier_name"])
    ety_output_path.insert(END, current_data["output_path"])

    batch_size = current_data["batch_size"]
    _dict_chk_var["_page_size_var"].set(batch_size["enable"])
    ety_page_size.insert(END, batch_size["path"])

    ety_A4_page_height.insert(END, batch_size["page_height_A4"])
    ety_A5_page_height.insert(END, batch_size["page_height_A5"])
    pass


def json_top_data(current_data):
    current_data["supplier_name"] = _widgets["ety_supplier_name"].get()
    current_data["output_path"] = _widgets["ety_output_path"].get()

    batch_size = current_data["batch_size"]
    batch_size["enable"] = _dict_chk_var["_page_size_var"].get()
    batch_size["path"] = _widgets["ety_page_size"].get()

    ety_A4_page_height = _widgets["ety_A4_page_height"].get()
    ety_A5_page_height = _widgets["ety_A5_page_height"].get()
    batch_size["page_height_A4"] = int(ety_A4_page_height) if ety_A4_page_height else 0
    batch_size["page_height_A5"] = int(ety_A5_page_height) if ety_A5_page_height else 0

    pass
