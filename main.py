from ttkbootstrap import Window, Notebook
from database import init_db
from ui_add_update import create_add_update_tab
from ui_view import create_view_tab
from utils import ensure_single_instance, cleanup_lock
from app_styles import setup_style
from ui_analysis import create_analysis_tab

def main():
    ensure_single_instance()
    app = Window(themename="superhero")
    setup_style(app)
    conn = init_db()

    notebook = Notebook(app, bootstyle="primary")
    notebook.pack(fill="both", expand=True, padx=15, pady=15)

    # Create the Add/Update tab first, so we can pass its filler function later
    add_tab, fill_form_callback = create_add_update_tab(
        notebook,
        conn,
        lambda: (
            view_tab.event_generate("<<Refresh>>"),
            notebook.select(view_tab)  # auto-switch to View tab after refresh
        )
    )

    
    # Pass that callback to the View tab
    view_tab = create_view_tab(notebook, conn, fill_form_callback, notebook)

    analysis_tab = create_analysis_tab(notebook)

    try:
        app.mainloop()
    finally:
        cleanup_lock()

if __name__ == "__main__":
    main()
