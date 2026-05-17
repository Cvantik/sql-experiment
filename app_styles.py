import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def setup_style(app):
    app.title("💼 Job Application Tracker")

    # Set the desired window size
    width, height = 950, 600
    app.geometry(f"{width}x{height}")

    # Center the window on screen
    app.update_idletasks()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

    # Background and resizing behavior
    app.configure(bg="#2b2b2b")
    app.resizable(False, False)
    
    # --- Header bar ---
    header = ttk.Label(
        app,
        text="💼 Job Application Tracker",
        font=("Segoe UI", 18, "bold"),
        bootstyle="inverse-dark",
        anchor="center"
    )
    header.pack(fill=X, pady=(10, 0))
