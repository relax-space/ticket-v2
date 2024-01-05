from tkinter import END, Entry
from relax.util import global_widgets


def json_ticket_data(current_data):
    ticket_mapping = current_data["ticket"]["mapping"]

    ticket_mapping["ticket_path"] = global_widgets["ety_ticket_folder"].get().strip()
    ticket_mapping["mapping_path"] = global_widgets["ety_ticket_mapping"].get().strip()
    ticket_mapping["exclude_zd"] = global_widgets["ety_exclude_ticket_zd"].get().strip()
    pass


def render_ticket_data(current_data):
    ticket_mapping = current_data["ticket"]["mapping"]
    ety_ticket_folder: Entry = global_widgets["ety_ticket_folder"]
    ety_ticket_folder.delete(0, END)
    ety_ticket_folder.insert(END, ticket_mapping["ticket_path"])

    ety_ticket_mapping: Entry = global_widgets["ety_ticket_mapping"]
    ety_ticket_mapping.delete(0, END)
    ety_ticket_mapping.insert(END, ticket_mapping["mapping_path"])

    ety_exclude_ticket_zd: Entry = global_widgets["ety_exclude_ticket_zd"]
    ety_exclude_ticket_zd.delete(0, END)
    ety_exclude_ticket_zd.insert(END, ticket_mapping["exclude_zd"])
    pass
