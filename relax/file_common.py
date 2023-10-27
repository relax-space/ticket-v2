from os import path as os_path
from shutil import copyfile
from xlsxwriter.worksheet import Worksheet
from pypdf import PdfReader, PdfWriter, Transformation, PaperSize

from relax.util import mm_to_pixel
from fitz import Document, paper_rect
from pdfCropMargins import crop
from time import sleep


def get_row_height_byrow(
    row_count: int,
    height1: int = 15,
    height2: int = 7,
    height3: int = 11,
) -> int:
    total_height = 0
    match row_count:
        case 0 | 1:
            total_height = height1
        case 2:
            total_height = height1 + height2
        case _:
            total_height = height1 + height2 + (row_count - 2) * height3
    return total_height


def get_row_count(raw: str, max_china_per_row: int = 17) -> tuple[int, str]:
    row_count = 1
    total_count = len(raw.encode("utf8"))
    char_count_per_row = max_china_per_row * 3
    if total_count <= char_count_per_row:
        """
        处理大多数数据
        """
        return row_count, raw
    else:
        break_list = []
        char_list = list(raw)
        i = 0
        current_char_count = 0
        char_count = len(char_list)
        while i < char_count:
            v = len(char_list[i].encode("utf8"))
            current_char_count += v
            if current_char_count > char_count_per_row:
                current_char_count = 0
                break_list.append(i)
                i -= 1
                row_count += 1
            i += 1

        new_content = ""
        break_list_count = len(break_list)
        for i, v in enumerate(break_list):
            if i == 0:
                new_content += raw[0:v] + "\n"
            else:
                new_content += raw[v : break_list[i + 1]] + "\n"
            if i == break_list_count - 1:
                new_content += raw[v:]
        return row_count, new_content


def get_row_height_content(
    raw: str,
    byte_per_row: int = 17,
    height1: int = 15,
    height2: int = 7,
    height3: int = 11,
):
    row_count, new_content = get_row_count(raw, byte_per_row)
    row_height = get_row_height_byrow(row_count, height1, height2, height3)
    return row_height, new_content


def set_page_size(ws1: Worksheet, size_dict: dict):
    page_size = size_dict["page_size"]
    page_size_index = 9
    if page_size == "A4":
        ws1.set_portrait()
    elif page_size == "A5":
        ws1.set_landscape()
        page_size_index = 11
    ws1.set_paper(page_size_index)
    return page_size


def make_stamp(ws1: Worksheet, row_height_list: list, page_height: int, stamp: dict):
    column = stamp["column"]
    img_path = stamp["path"]
    x_scale = stamp["x_scale"]
    y_scale = stamp["y_scale"]
    x_offset = stamp["x_offset"]
    y_offset = stamp["y_offset"]
    page_count = 1
    total_height = 0
    break_list = []
    current_height = 0
    page_height_but_last = 0
    for height in row_height_list:
        total_height += height

    i = 0
    row_count = len(row_height_list)
    while i < row_count:
        v = row_height_list[i]
        current_height += v
        page_height_but_last += v
        if current_height > page_height:
            current_height = 0
            page_height_but_last -= v
            i -= 1
            break_list.append(i)
            page_count += 1
        i += 1

    # 保证最后一页，至少有两行数据
    rest_height = total_height - page_height_but_last
    if rest_height == row_height_list[-1]:
        if break_list:
            break_list.pop()
        break_list.append(row_count - 2)

    dic_img = {
        "x_scale": x_scale,
        "y_scale": y_scale,
        "x_offset": x_offset,
        "y_offset": y_offset,
    }

    ws1.insert_image(
        f"{column}2",
        img_path,
        dic_img,
    )
    for i in break_list:
        ws1.insert_image(
            f"{column}{i+1}",
            img_path,
            dic_img,
        )
    ws1.set_h_pagebreaks(break_list)
    pass


def make_print_file_one(
    zd: str,
    page_size: str,
    page_quantity: int,
    source_path: str,
    target_path: str,
    order_mark: str,
    postfix: str,
    callback,
    zd_seq: int = 1,
):
    for i in range(page_quantity):
        target_name = callback(zd, i, order_mark, page_size, postfix, zd_seq)
        target_path_name = os_path.join(target_path, target_name)
        copyfile(source_path, target_path_name)


def pdf_to_landscape_pure(source_file_path: str, target_file_path: str, page_size: str):
    source_doc = Document(source_file_path)
    target_doc = Document()
    for ipage in source_doc:
        rect = paper_rect(f"{page_size}-l")
        page = target_doc.new_page(width=rect.width, height=rect.height)
        page.show_pdf_page(rect, source_doc, ipage.number)
    source_doc.close()
    target_doc.save(target_file_path)
    pass


def pdf_crop(
    source_file_path: str,
    target_file_path: str,
    left_margin,
    bottom_margin,
    right_margin,
    up_margin,
):
    output_path, exit_code, _, _ = crop(
        [
            "--absoluteOffset4",
            f"{left_margin}",
            f"{bottom_margin}",
            f"{right_margin}",
            f"{up_margin}",
            "-o",
            target_file_path,
            "-u",
            "-s",
            source_file_path,
        ],
        string_io=True,
        quiet=True,
    )
    return output_path, exit_code


def pdf_to_landscape(
    source_path: str,
    target_path: str,
    target_path_crop: str,
    file_name_with_postfix: str,
    margin_dict: dict,
    page_size: str,
):
    source_file_path = os_path.join(source_path, file_name_with_postfix)
    t1 = os_path.join(target_path_crop, file_name_with_postfix)
    left, right, top, bottom = (
        -mm_to_pixel(margin_dict["left"]),
        -mm_to_pixel(margin_dict["right"]),
        -mm_to_pixel(margin_dict["top"]),
        -mm_to_pixel(margin_dict["bottom"]),
    )
    _, error = pdf_crop(source_file_path, t1, left, bottom, right, top)
    if error:
        return False
    t2 = os_path.join(target_path, file_name_with_postfix)
    pdf_to_landscape_pure(t1, t2, page_size)
    return True


def pdf_to_portrait(
    source_path: str,
    target_path: str,
    file_name_with_postfix: str,
    margin_dict: dict,
    page_size: str,
):
    source_file_path = os_path.join(source_path, file_name_with_postfix)
    with open(source_file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        left, right, top, bottom = (
            mm_to_pixel(margin_dict["left"]),
            mm_to_pixel(margin_dict["right"]),
            mm_to_pixel(margin_dict["top"]),
            mm_to_pixel(margin_dict["bottom"]),
        )
        target_width = PaperSize.A4.width if page_size == "A4" else PaperSize.A5.width
        target_height = (
            PaperSize.A4.height if page_size == "A4" else PaperSize.A5.height
        )
        pdf_write = PdfWriter()
        for page in pdf_reader.pages:
            page_width = page.mediabox.width
            page_height = page.mediabox.height
            scale_factor = min(
                (target_width - (left + right)) / page_width,
                (target_height - (top + bottom)) / page_height,
            )
            blank = pdf_write.add_blank_page(width=target_width, height=target_height)
            ty = target_height - page_height * scale_factor - top
            blank.merge_transformed_page(
                page,
                Transformation()
                .scale(
                    scale_factor,
                    scale_factor,
                )
                .translate(left, ty),
            )
            pass
    with open(os_path.join(target_path, file_name_with_postfix), mode="wb") as f_write:
        pdf_write.write(f_write)
    pass


def scale_pdf_size(
    source_path: str,
    target_path: str,
    target_path_crop: str,
    file_name_with_postfix: str,
    margin_dict: dict,
    page_size: str,
    page_orient: str,
):
    a4, a5 = "A4", "A5"
    if (not page_size) or (page_size not in [a4, a5]):
        return
    if page_orient == "p":
        pdf_to_portrait(
            source_path,
            target_path,
            file_name_with_postfix,
            margin_dict,
            page_size,
        )
        return True
    else:
        return pdf_to_landscape(
            source_path,
            target_path,
            target_path_crop,
            file_name_with_postfix,
            margin_dict,
            page_size,
        )

    pass
