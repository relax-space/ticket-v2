from tkinter import END, Checkbutton, Entry
from relax.util_win import _widgets, _dict_chk_var


def json_template_input(current_data: dict):
    product_input = current_data["product"]["input"]
    batch_import = product_input["batch_import"]
    batch_import["enable"] = _dict_chk_var["_import_var"].get()
    batch_import["path"] = _widgets["ety_import"].get()

    stamp = product_input["stamp"]
    stamp["enable"] = _dict_chk_var["_stamp_var"].get()
    stamp["path"] = _widgets["ety_stamp"].get()
    ety_X_stamp_scale = _widgets["ety_X_stamp_scale"].get()
    ety_Y_stamp_scale = _widgets["ety_Y_stamp_scale"].get()
    stamp["x_scale"] = float(ety_X_stamp_scale) if ety_X_stamp_scale else 0.0
    stamp["y_scale"] = float(ety_Y_stamp_scale) if ety_Y_stamp_scale else 0.0

    pass


def json_template_output_cover(current_data: dict):
    ety_row_height_cover_1: Entry = _widgets[f"ety_row_height_cover_0"]
    ety_row_height_cover_2: Entry = _widgets[f"ety_row_height_cover_1"]
    ety_row_height_cover_3: Entry = _widgets[f"ety_row_height_cover_2"]
    ety_row_height_cover_4: Entry = _widgets[f"ety_row_height_cover_3"]
    ety_row_height_cover_5: Entry = _widgets[f"ety_row_height_cover_4"]

    cover = current_data["product"]["output"]["cover"]
    cover_column_width = cover["column_width"]
    for i in ["A", "B", "C"]:
        ety_column_width_cover = _widgets[f"ety_column_width_cover_{i}"].get()
        cover_column_width[i] = (
            float(ety_column_width_cover) if ety_column_width_cover else 0
        )

    ety_row_height_cover_1 = ety_row_height_cover_1.get()
    ety_row_height_cover_2 = ety_row_height_cover_2.get()
    ety_row_height_cover_3 = ety_row_height_cover_3.get()
    ety_row_height_cover_4 = ety_row_height_cover_4.get()
    ety_row_height_cover_5 = ety_row_height_cover_5.get()

    cover["row1"]["height"] = (
        int(ety_row_height_cover_1) if ety_row_height_cover_1 else 0
    )
    cover["row2"]["height"] = (
        int(ety_row_height_cover_2) if ety_row_height_cover_2 else 0
    )
    cover["row3"]["height"] = (
        int(ety_row_height_cover_3) if ety_row_height_cover_3 else 0
    )
    cover["row_data"]["height"] = (
        int(ety_row_height_cover_4) if ety_row_height_cover_4 else 0
    )
    cover["row_last"]["height"] = (
        int(ety_row_height_cover_5) if ety_row_height_cover_5 else 0
    )
    pass


def json_template_output_product(current_data: dict):
    ety_row_height_product_1: Entry = _widgets[f"ety_row_height_product_0"]
    ety_row_height_product_2: Entry = _widgets[f"ety_row_height_product_1"]
    ety_row_height_product_3: Entry = _widgets[f"ety_row_height_product_2"]
    ety_row_height_product_4: Entry = _widgets[f"ety_row_height_product_3"]
    ety_row_height_product_5: Entry = _widgets[f"ety_row_height_product_4"]
    ety_row_height_product_6: Entry = _widgets[f"ety_row_height_product_5"]
    ety_row_height_product_7: Entry = _widgets[f"ety_row_height_product_6"]
    ety_row_height_product_8: Entry = _widgets[f"ety_row_height_product_7"]

    product_detail = current_data["product"]["output"]["product_detail"]
    product_column_width = product_detail["column_width"]
    for i in ["A", "B", "C", "D", "E", "C", "F", "G", "H"]:
        ety_column_width_product = _widgets[f"ety_column_width_product_{i}"].get()
        product_column_width[i] = (
            float(ety_column_width_product) if ety_column_width_product else 0
        )
    ety_row_height_product_1 = ety_row_height_product_1.get()
    ety_row_height_product_2 = ety_row_height_product_2.get()
    ety_row_height_product_3 = ety_row_height_product_3.get()
    ety_row_height_product_4 = ety_row_height_product_4.get()
    ety_row_height_product_5 = ety_row_height_product_5.get()
    ety_row_height_product_6 = ety_row_height_product_6.get()
    ety_row_height_product_7 = ety_row_height_product_7.get()
    ety_row_height_product_8 = ety_row_height_product_8.get()

    product_detail["row1"]["height"] = (
        int(ety_row_height_product_1) if ety_row_height_product_1 else 0
    )
    product_detail["row2"]["height"] = (
        int(ety_row_height_product_2) if ety_row_height_product_2 else 0
    )
    product_detail["row3"]["height"] = (
        int(ety_row_height_product_3) if ety_row_height_product_3 else 0
    )
    product_detail["row4"]["height"] = (
        int(ety_row_height_product_4) if ety_row_height_product_4 else 0
    )
    product_detail["row_data"]["height"] = (
        int(ety_row_height_product_5) if ety_row_height_product_5 else 0
    )
    product_detail["row_sum_1"]["height"] = (
        int(ety_row_height_product_6) if ety_row_height_product_6 else 0
    )
    product_detail["row_sum_2"]["height"] = (
        int(ety_row_height_product_7) if ety_row_height_product_7 else 0
    )
    product_detail["row_last"]["height"] = (
        int(ety_row_height_product_8) if ety_row_height_product_8 else 0
    )

    pass


def render_input(current_data: dict):
    ety_product_input: Entry = _widgets["ety_product_input"]
    ety_import: Entry = _widgets["ety_import"]
    ety_stamp: Entry = _widgets["ety_stamp"]
    ety_X_stamp_scale: Entry = _widgets["ety_X_stamp_scale"]
    ety_Y_stamp_scale: Entry = _widgets["ety_Y_stamp_scale"]

    product_input = current_data["product"]["input"]
    ety_product_input.delete(0, END)
    ety_product_input.insert(END, product_input["product_path"])
    batch_import = product_input["batch_import"]
    _dict_chk_var["_import_var"].set(batch_import["enable"])
    ety_import.delete(0, END)
    ety_import.insert(END, batch_import["path"])

    stamp = product_input["stamp"]
    _dict_chk_var["_stamp_var"].set(stamp["enable"])
    ety_stamp.delete(0, END)
    ety_stamp.insert(END, stamp["path"])
    ety_X_stamp_scale.delete(0, END)
    ety_X_stamp_scale.insert(END, stamp["x_scale"])
    ety_Y_stamp_scale.delete(0, END)
    ety_Y_stamp_scale.insert(END, stamp["y_scale"])

    pass


def render_output_cover(current_data: dict):
    ety_row_height_cover_1: Entry = _widgets[f"ety_row_height_cover_0"]
    ety_row_height_cover_2: Entry = _widgets[f"ety_row_height_cover_1"]
    ety_row_height_cover_3: Entry = _widgets[f"ety_row_height_cover_2"]
    ety_row_height_cover_4: Entry = _widgets[f"ety_row_height_cover_3"]
    ety_row_height_cover_5: Entry = _widgets[f"ety_row_height_cover_4"]

    cover = current_data["product"]["output"]["cover"]
    cover_column_width = cover["column_width"]
    for i in ["A", "B", "C"]:
        _widgets[f"ety_column_width_cover_{i}"].delete(0, END)
        _widgets[f"ety_column_width_cover_{i}"].insert(END, cover_column_width[i])

    ety_row_height_cover_1.delete(0, END)
    ety_row_height_cover_2.delete(0, END)
    ety_row_height_cover_3.delete(0, END)
    ety_row_height_cover_4.delete(0, END)
    ety_row_height_cover_5.delete(0, END)
    ety_row_height_cover_1.insert(END, cover["row1"]["height"])
    ety_row_height_cover_2.insert(END, cover["row2"]["height"])
    ety_row_height_cover_3.insert(END, cover["row3"]["height"])
    ety_row_height_cover_4.insert(END, cover["row_data"]["height"])
    ety_row_height_cover_5.insert(END, cover["row_last"]["height"])
    pass


def render_output_product(current_data: dict):
    ety_row_height_product_1: Entry = _widgets[f"ety_row_height_product_0"]
    ety_row_height_product_2: Entry = _widgets[f"ety_row_height_product_1"]
    ety_row_height_product_3: Entry = _widgets[f"ety_row_height_product_2"]
    ety_row_height_product_4: Entry = _widgets[f"ety_row_height_product_3"]
    ety_row_height_product_5: Entry = _widgets[f"ety_row_height_product_4"]
    ety_row_height_product_6: Entry = _widgets[f"ety_row_height_product_5"]
    ety_row_height_product_7: Entry = _widgets[f"ety_row_height_product_6"]
    ety_row_height_product_8: Entry = _widgets[f"ety_row_height_product_7"]

    product_detail = current_data["product"]["output"]["product_detail"]
    product_column_width = product_detail["column_width"]
    for i in ["A", "B", "C", "D", "E", "C", "F", "G", "H"]:
        _widgets[f"ety_column_width_product_{i}"].delete(0, END)
        _widgets[f"ety_column_width_product_{i}"].insert(END, product_column_width[i])

    ety_row_height_product_1.delete(0, END)
    ety_row_height_product_2.delete(0, END)
    ety_row_height_product_3.delete(0, END)
    ety_row_height_product_4.delete(0, END)
    ety_row_height_product_5.delete(0, END)
    ety_row_height_product_6.delete(0, END)
    ety_row_height_product_7.delete(0, END)
    ety_row_height_product_8.delete(0, END)
    ety_row_height_product_1.insert(END, product_detail["row1"]["height"])
    ety_row_height_product_2.insert(END, product_detail["row2"]["height"])
    ety_row_height_product_3.insert(END, product_detail["row3"]["height"])
    ety_row_height_product_4.insert(END, product_detail["row4"]["height"])
    ety_row_height_product_5.insert(END, product_detail["row_data"]["height"])
    ety_row_height_product_6.insert(END, product_detail["row_sum_1"]["height"])
    ety_row_height_product_7.insert(END, product_detail["row_sum_2"]["height"])
    ety_row_height_product_8.insert(END, product_detail["row_last"]["height"])

    pass


def render_product_data(current_data):
    render_input(current_data)
    render_output_cover(current_data)
    render_output_product(current_data)
    pass


def json_product_data(current_data):
    json_template_input(current_data)
    json_template_output_cover(current_data)
    json_template_output_product(current_data)
