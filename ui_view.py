import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import fetch_applications, delete_application

def create_view_tab(notebook, conn, fill_form_callback=None, notebook_ref=None):
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="View Applications")

    columns = ('id', 'company', 'position', 'date_applied', 'status', 'location', 'contact_person', 'notes')
    tree = ttk.Treeview(tab, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, width=120)
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

    def refresh(_event=None):  # accept event argument if triggered by event_generate
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_applications(conn):
            tree.insert("", "end", values=row)

    # 🟩 Bind custom refresh event
    tab.bind("<<Refresh>>", refresh)

    # 🟩 Also refresh once at startup
    refresh()
    
    # 🟩 Handle double-click event
    def on_double_click(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, 'values')
        if not values:
            return

        data = dict(
            id=values[0],
            company=values[1],
            position=values[2],
            date_applied=values[3],
            status=values[4],
            location=values[5],
            contact_person=values[6],
            notes=values[7]
        )

        if fill_form_callback:
            fill_form_callback(data)

        if notebook_ref:
            notebook_ref.select(0)  # Switch to Add/Update tab

    tree.bind("<Double-1>", on_double_click)

    ttk.Button(tab, text="Delete Selected", bootstyle="danger", command=lambda: _on_delete(tree, conn, refresh)).pack(pady=10)

    refresh()
    return tab

def _on_delete(tree, conn, refresh):
    selected = tree.focus()
    if not selected:
        from tkinter import messagebox
        messagebox.showwarning("Select Entry", "Please select a row to delete.")
        return
    data = tree.item(selected, 'values')
    delete_application(conn, data[0])
    refresh()
