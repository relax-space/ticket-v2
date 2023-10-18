from relax.product_win_data import json_product_data, render_product_data
from relax.ticket_win_data import json_ticket_data, render_ticket_data
from relax.top_win_data import json_top_data, render_top_data


def render_data(current_data):
    """
    将current_data数据填充到界面
    """
    render_top_data(current_data)
    render_product_data(current_data)
    render_ticket_data(current_data)


def json_data(current_data):
    """
    将界面数据填充到current_data
    """
    json_top_data(current_data)
    json_product_data(current_data)
    json_ticket_data(current_data)


