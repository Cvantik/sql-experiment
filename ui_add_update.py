from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import Canvas
from utils import meme_popup
from database import add_application, update_application
from database import get_status_distribution


def create_add_update_tab(notebook, conn, refresh_table_callback):
    tab = ttk.Frame(notebook, padding=20)
    notebook.add(tab, text="Add / Update Application")

    company_var = ttk.StringVar()
    position_var = ttk.StringVar()
    status_var = ttk.StringVar(value="Applied")
    location_var = ttk.StringVar()
    contact_var = ttk.StringVar()
    notes_var = ttk.StringVar()

    # Track the ID of the application being edited
    current_app_id = [None]

    # --- Date split dropdowns ---
    day_var = ttk.StringVar(value=datetime.today().strftime('%d'))
    month_var = ttk.StringVar(value=datetime.today().strftime('%m'))
    year_var = ttk.StringVar(value=datetime.today().strftime('%Y'))

    # --- Combined layout frame for left form + right status bar ---
    content_frame = ttk.Frame(tab)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Left side: Application Details form ---
    form_frame = ttk.Labelframe(content_frame, text="Application Details", bootstyle="secondary", padding=15)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    # Helper for consistent widget width
    ENTRY_WIDTH = 55
    COMBO_WIDTH = 53

    # --- Company ---
    ttk.Label(form_frame, text="Company", bootstyle="light").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    ttk.Entry(form_frame, textvariable=company_var, width=ENTRY_WIDTH).grid(row=0, column=1, padx=10, pady=5, sticky=W)

    # --- Position ---
    ttk.Label(form_frame, text="Position", bootstyle="light").grid(row=1, column=0, sticky=W, padx=10, pady=5)
    positions = ["Receptionist", "Pilot", "Programming"]
    ttk.Combobox(form_frame, textvariable=position_var, values=positions, width=COMBO_WIDTH).grid(row=1, column=1, padx=10, pady=5, sticky=W)

    # --- Date Applied ---
    ttk.Label(form_frame, text="Date Applied", bootstyle="light").grid(row=2, column=0, sticky=W, padx=10, pady=5)
    date_frame = ttk.Frame(form_frame)
    date_frame.grid(row=2, column=1, sticky=W, padx=10, pady=5)
    days = [str(d).zfill(2) for d in range(1, 32)]
    months = [str(m).zfill(2) for m in range(1, 13)]
    years = [str(y) for y in range(2024, datetime.today().year + 1)]
    ttk.Combobox(date_frame, textvariable=day_var, values=days, width=5).pack(side="left", padx=2)
    ttk.Combobox(date_frame, textvariable=month_var, values=months, width=5).pack(side="left", padx=2)
    ttk.Combobox(date_frame, textvariable=year_var, values=years, width=7).pack(side="left", padx=2)

    # --- Status ---
    ttk.Label(form_frame, text="Status", bootstyle="light").grid(row=3, column=0, sticky=W, padx=10, pady=5)
    statuses = ["Applied", "Negotiating", "No Response", "Rejected"]
    ttk.Combobox(form_frame, textvariable=status_var, values=statuses, width=COMBO_WIDTH).grid(row=3, column=1, padx=10, pady=5, sticky=W)

    # --- Location ---
    ttk.Label(form_frame, text="Location", bootstyle="light").grid(row=4, column=0, sticky=W, padx=10, pady=5)
    locations = ["Prague", "Outside", "Abroad"]
    ttk.Combobox(form_frame, textvariable=location_var, values=locations, width=COMBO_WIDTH).grid(row=4, column=1, padx=10, pady=5, sticky=W)

    # --- Contact Person ---
    ttk.Label(form_frame, text="Contact Person", bootstyle="light").grid(row=5, column=0, sticky=W, padx=10, pady=5)
    ttk.Entry(form_frame, textvariable=contact_var, width=ENTRY_WIDTH).grid(row=5, column=1, padx=10, pady=5, sticky=W)

    # --- Notes ---
    ttk.Label(form_frame, text="Notes", bootstyle="light").grid(row=6, column=0, sticky=W, padx=10, pady=5)
    ttk.Entry(form_frame, textvariable=notes_var, width=ENTRY_WIDTH).grid(row=6, column=1, padx=10, pady=5, sticky=W)
    
    # --- Button Row ---
    button_frame = ttk.Frame(form_frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=15)

    # --- Add Function ---
    def on_add():
        try:
            date = datetime.strptime(f"{year_var.get()}-{month_var.get()}-{day_var.get()}", "%Y-%m-%d").date()
            if date > datetime.today().date():
                meme_popup("Invalid Date", "Future dates are not allowed.")
                return

            data = (
                company_var.get(), position_var.get(), date.strftime("%Y-%m-%d"),
                status_var.get(), location_var.get(), contact_var.get(), notes_var.get()
            )
            add_application(conn, data)
            messagebox.showinfo("Added", "Application added successfully!")
            refresh_table_callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        update_status_bar()

    # --- Update Function ---
    def on_update():
        try:
            if not current_app_id[0]:
                messagebox.showwarning("No Selection", "Please double-click an entry in the View tab first.")
                return

            date = datetime.strptime(f"{year_var.get()}-{month_var.get()}-{day_var.get()}", "%Y-%m-%d").date()
            if date > datetime.today().date():
                meme_popup("Invalid Date", "Future dates are not allowed.")
                return

            data = (
                company_var.get(), position_var.get(), date.strftime("%Y-%m-%d"),
                status_var.get(), location_var.get(), contact_var.get(), notes_var.get()
            )

            update_application(conn, data, current_app_id[0])
            messagebox.showinfo("Updated", "Application updated successfully!")
            refresh_table_callback()

            # Clear form and reset ID
            for v in [company_var, position_var, location_var, contact_var, notes_var]:
                v.set("")
            status_var.set("Applied")
            current_app_id[0] = None

        except Exception as e:
            messagebox.showerror("Error", str(e))
        update_status_bar()

    # --- Clear Function ---
    def on_clear():
        for v in [company_var, position_var, location_var, contact_var, notes_var]:
            v.set("")
        status_var.set("Applied")
        current_app_id[0] = None

    # --- Buttons ---
    ttk.Button(button_frame, text="➕ Add", command=on_add, bootstyle="success", width=16).pack(side="left", padx=10)
    ttk.Button(button_frame, text="📝 Update", command=on_update, bootstyle="info", width=16).pack(side="left", padx=10)
    ttk.Button(button_frame, text="🧹 Clear", command=on_clear, bootstyle="danger", width=16).pack(side="left", padx=10)

    # --- Fill Form Function (called from View tab) ---
    def fill_form(data):
        """Fill the form fields with data from a selected row."""
        company_var.set(data.get("company", ""))
        position_var.set(data.get("position", ""))
        status_var.set(data.get("status", "Applied"))
        location_var.set(data.get("location", ""))
        contact_var.set(data.get("contact_person", ""))
        notes_var.set(data.get("notes", ""))

        date_str = data.get("date_applied")
        if date_str:
            try:
                y, m, d = date_str.split("-")
                year_var.set(y)
                month_var.set(m)
                day_var.set(d)
            except Exception:
                pass

        current_app_id[0] = data.get("id")

    # --- Status Overview Section ---
    overview_frame = ttk.Labelframe(content_frame, text="Status Overview", bootstyle="secondary", padding=15)
    overview_frame.grid(row=0, column=1, sticky="n", padx=(10, 5), pady=(0, 5))

    # Subframes: bar on left, legend on right
    bar_frame = ttk.Frame(overview_frame)
    bar_frame.grid(row=0, column=0, sticky="n")

    legend_frame = ttk.Frame(overview_frame, width=150, height=350)
    legend_frame.grid(row=0, column=1, sticky="nw", padx=10)
    legend_frame.grid_propagate(False)


    content_frame.columnconfigure(0, weight=3)
    content_frame.columnconfigure(1, weight=1)

    # --- Canvas for the vertical bar ---
    canvas_width = 70
    canvas_height = 350
    status_canvas = Canvas(
        bar_frame,
        width=canvas_width,
        height=canvas_height,
        bg="#2b2b2b",
        highlightthickness=1,
        highlightbackground="#404040"
    )
    status_canvas.pack()

    # --- Colors for each status ---
    status_colors = {
        "Applied": "#4FC3F7",       # light blue
        "Negotiating": "#FFD54F",   # gold
        "No Response": "#FFB74D",   # orange
        "Rejected": "#E57373",      # red
        "Other": "#B0BEC5"          # gray
    }


    def update_status_bar():
        """Draw vertical progress bar sorted top-to-bottom with aligned right-side labels."""
        status_canvas.delete("all")
        for widget in legend_frame.winfo_children():
            widget.destroy()

        data = get_status_distribution(conn)
        total = sum(data.values())
        if total == 0:
            return

        # --- Define display order ---
        status_order = ["Applied", "Negotiating", "No Response", "Rejected"]
        ordered_data = []

        # Add known statuses first
        for key in status_order:
            if key in data:
                ordered_data.append((key, data[key]))

        # Add any remaining custom statuses (as Other)
        for key, val in data.items():
            if key not in status_order:
                ordered_data.append((key, val))

        # --- Draw segments from top to bottom in defined order ---
        y_offset = 0
        for status, count in ordered_data:
            fraction = count / total
            seg_height = int(canvas_height * fraction)
            y_bottom = y_offset + seg_height
            color = status_colors.get(status, status_colors["Other"])

            # --- Draw colored rectangle ---
            status_canvas.create_rectangle(
                10, y_offset, canvas_width - 10, y_bottom,
                fill=color, outline="#1c1c1c"
            )

            # --- Add percentage text inside segment ---
            percent_text = f"{int(fraction * 100)}%"
            if seg_height >= 18:
                status_canvas.create_text(
                    canvas_width / 2,
                    (y_offset + y_bottom) / 2,
                    text=percent_text,
                    fill="white",
                    font=("Segoe UI", 9, "bold")
                )

            # --- Arrow midpoint ---
            mid_y = (y_offset + y_bottom) / 2

            # --- Draw arrow pointing right ---
            status_canvas.create_line(
                canvas_width - 10, mid_y, canvas_width + 15, mid_y,
                fill="white", width=2, arrow="last"
            )

            # --- Align label beside arrow ---
            legend_item = ttk.Frame(legend_frame)
            legend_item.place(x=0, y=mid_y - 10)
            ttk.Label(legend_item, text=status, bootstyle="light").pack(side="left")

            # Move offset down for next segment
            y_offset = y_bottom



    # Initialize once on tab load
    update_status_bar()
    return tab, fill_form
