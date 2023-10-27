from tkinter import END, Entry
from relax.util import global_widgets, global_dict_chk_var


def json_template_input(current_data: dict):
    import_list = current_data["product"]["output"]["import_list"]
    import_list["enable"] = global_dict_chk_var["_import_var"].get()
    import_list["path"] = global_widgets["ety_import"].get()
    v = global_dict_chk_var["_import_var_option"].get()
    import_list["default_value"] = v

    current_import = import_list[v]
    current_import["sale_name"] = global_widgets["ety_sale_name"].get()
    current_import["sale_account"] = global_widgets["ety_sale_account"].get()
    current_import["exclude_zd"] = global_widgets["ety_exclude_zd"].get()
    header_max = global_widgets["ety_header_max"].get()
    detail_max = global_widgets["ety_detail_max"].get()
    current_import["header_max"] = int(header_max) if header_max else ""
    current_import["detail_max"] = int(detail_max) if detail_max else ""

    product_input = current_data["product"]["input"]
    product_input["product_path"] = global_widgets["ety_product_input"].get()
    stamp = product_input["stamp"]
    stamp["enable"] = global_dict_chk_var["_stamp_var"].get()
    stamp["path"] = global_widgets["ety_stamp"].get()
    ety_X_stamp_scale_cover = global_widgets["ety_X_stamp_scale_cover"].get()
    ety_Y_stamp_scale_cover = global_widgets["ety_Y_stamp_scale_cover"].get()
    stamp_cover = stamp["cover"]
    stamp_cover["x_scale"] = (
        float(ety_X_stamp_scale_cover) if ety_X_stamp_scale_cover else 0.0
    )
    stamp_cover["y_scale"] = (
        float(ety_Y_stamp_scale_cover) if ety_Y_stamp_scale_cover else 0.0
    )

    ety_X_stamp_scale_product = global_widgets["ety_X_stamp_scale_product"].get()
    ety_Y_stamp_scale_product = global_widgets["ety_Y_stamp_scale_product"].get()
    stamp_product = stamp["product"]
    stamp_product["x_scale"] = (
        float(ety_X_stamp_scale_product) if ety_X_stamp_scale_product else 0.0
    )
    stamp_product["y_scale"] = (
        float(ety_Y_stamp_scale_product) if ety_Y_stamp_scale_product else 0.0
    )

    pass


def json_template_output_cover(current_data: dict):
    ety_row_height_cover_1: Entry = global_widgets[f"ety_row_height_cover_0"]
    ety_row_height_cover_2: Entry = global_widgets[f"ety_row_height_cover_1"]
    ety_row_height_cover_3: Entry = global_widgets[f"ety_row_height_cover_2"]
    ety_row_height_cover_4: Entry = global_widgets[f"ety_row_height_cover_3"]
    ety_row_height_cover_5: Entry = global_widgets[f"ety_row_height_cover_4"]

    cover = current_data["product"]["output"]["cover"]
    cover_column_width = cover["column_width"]
    for i in ["A", "B", "C"]:
        ety_column_width_cover = global_widgets[f"ety_column_width_cover_{i}"].get()
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
    ety_row_height_product_1: Entry = global_widgets[f"ety_row_height_product_0"]
    ety_row_height_product_2: Entry = global_widgets[f"ety_row_height_product_1"]
    ety_row_height_product_3: Entry = global_widgets[f"ety_row_height_product_2"]
    ety_row_height_product_4: Entry = global_widgets[f"ety_row_height_product_3"]
    ety_row_height_product_5: Entry = global_widgets[f"ety_row_height_product_4"]
    ety_row_height_product_6: Entry = global_widgets[f"ety_row_height_product_5"]
    ety_row_height_product_7: Entry = global_widgets[f"ety_row_height_product_6"]
    ety_row_height_product_8: Entry = global_widgets[f"ety_row_height_product_7"]

    product_detail = current_data["product"]["output"]["product_detail"]
    product_column_width = product_detail["column_width"]
    for i in ["A", "B", "C", "D", "E", "C", "F", "G", "H"]:
        ety_column_width_product = global_widgets[f"ety_column_width_product_{i}"].get()
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
    ety_product_input: Entry = global_widgets["ety_product_input"]
    ety_import: Entry = global_widgets["ety_import"]
    ety_sale_name: Entry = global_widgets["ety_sale_name"]
    ety_sale_account: Entry = global_widgets["ety_sale_account"]
    ety_exclude_zd: Entry = global_widgets["ety_exclude_zd"]
    ety_header_max: Entry = global_widgets["ety_header_max"]
    ety_detail_max: Entry = global_widgets["ety_detail_max"]

    ety_stamp: Entry = global_widgets["ety_stamp"]
    ety_X_stamp_scale_cover: Entry = global_widgets["ety_X_stamp_scale_cover"]
    ety_Y_stamp_scale_cover: Entry = global_widgets["ety_Y_stamp_scale_cover"]

    ety_X_stamp_scale_product: Entry = global_widgets["ety_X_stamp_scale_product"]
    ety_Y_stamp_scale_product: Entry = global_widgets["ety_Y_stamp_scale_product"]

    import_list = current_data["product"]["output"]["import_list"]
    global_dict_chk_var["_import_var"].set(import_list["enable"])
    ety_import.delete(0, END)
    ety_import.insert(END, import_list["path"])
    v = import_list["default_value"]
    global_dict_chk_var["_import_var_option"].set(v)
    current_import = import_list[v]
    sale_name = current_import.get("sale_name")
    sale_account = current_import.get("sale_account")
    exclude_zd = current_import.get("exclude_zd")
    header_max = current_import.get("header_max")
    detail_max = current_import.get("detail_max")
    if sale_name:
        ety_sale_name.delete(0, END)
        ety_sale_name.insert(END, sale_name)
    if sale_account:
        ety_sale_account.delete(0, END)
        ety_sale_account.insert(END, sale_account)
    if exclude_zd:
        ety_exclude_zd.delete(0, END)
        ety_exclude_zd.insert(END, exclude_zd)
    if header_max:
        ety_header_max.delete(0, END)
        ety_header_max.insert(END, header_max)
    if detail_max:
        ety_detail_max.delete(0, END)
        ety_detail_max.insert(END, detail_max)

    product_input = current_data["product"]["input"]
    ety_product_input.delete(0, END)
    ety_product_input.insert(END, product_input["product_path"])

    stamp = product_input["stamp"]
    global_dict_chk_var["_stamp_var"].set(stamp["enable"])
    ety_stamp.delete(0, END)
    ety_stamp.insert(END, stamp["path"])

    stamp_cover = stamp["cover"]
    ety_X_stamp_scale_cover.delete(0, END)
    ety_X_stamp_scale_cover.insert(END, stamp_cover["x_scale"])
    ety_Y_stamp_scale_cover.delete(0, END)
    ety_Y_stamp_scale_cover.insert(END, stamp_cover["y_scale"])

    stamp_product = stamp["product"]
    ety_X_stamp_scale_product.delete(0, END)
    ety_X_stamp_scale_product.insert(END, stamp_product["x_scale"])
    ety_Y_stamp_scale_product.delete(0, END)
    ety_Y_stamp_scale_product.insert(END, stamp_product["y_scale"])

    pass


def render_output_cover(current_data: dict):
    ety_row_height_cover_1: Entry = global_widgets[f"ety_row_height_cover_0"]
    ety_row_height_cover_2: Entry = global_widgets[f"ety_row_height_cover_1"]
    ety_row_height_cover_3: Entry = global_widgets[f"ety_row_height_cover_2"]
    ety_row_height_cover_4: Entry = global_widgets[f"ety_row_height_cover_3"]
    ety_row_height_cover_5: Entry = global_widgets[f"ety_row_height_cover_4"]

    cover = current_data["product"]["output"]["cover"]
    cover_column_width = cover["column_width"]
    for i in ["A", "B", "C"]:
        global_widgets[f"ety_column_width_cover_{i}"].delete(0, END)
        global_widgets[f"ety_column_width_cover_{i}"].insert(END, cover_column_width[i])

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
    ety_row_height_product_1: Entry = global_widgets[f"ety_row_height_product_0"]
    ety_row_height_product_2: Entry = global_widgets[f"ety_row_height_product_1"]
    ety_row_height_product_3: Entry = global_widgets[f"ety_row_height_product_2"]
    ety_row_height_product_4: Entry = global_widgets[f"ety_row_height_product_3"]
    ety_row_height_product_5: Entry = global_widgets[f"ety_row_height_product_4"]
    ety_row_height_product_6: Entry = global_widgets[f"ety_row_height_product_5"]
    ety_row_height_product_7: Entry = global_widgets[f"ety_row_height_product_6"]
    ety_row_height_product_8: Entry = global_widgets[f"ety_row_height_product_7"]

    product_detail = current_data["product"]["output"]["product_detail"]
    product_column_width = product_detail["column_width"]
    for i in ["A", "B", "C", "D", "E", "C", "F", "G", "H"]:
        global_widgets[f"ety_column_width_product_{i}"].delete(0, END)
        global_widgets[f"ety_column_width_product_{i}"].insert(
            END, product_column_width[i]
        )

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
