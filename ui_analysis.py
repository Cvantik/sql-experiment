# --- ui_analysis.py ---

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database import get_connection

def create_analysis_tab(notebook):
    tab_analysis = ttk.Frame(notebook, padding=10)
    notebook.add(tab_analysis, text="Analysis")

    analysis_frame = ttk.Labelframe(tab_analysis, text="Summary", bootstyle="secondary")
    analysis_frame.pack(fill=BOTH, expand=True, padx=15)

    analysis_text = ttk.Text(analysis_frame, width=80, height=15)
    analysis_text.pack(expand=True, fill=BOTH, padx=10, pady=10)

    ttk.Button(analysis_frame, text="Show Analysis", command=lambda: show_analysis(analysis_text), bootstyle="info", width=20).pack(pady=10)
    return tab_analysis


def show_analysis(analysis_text):
    conn, c = get_connection()
    analysis_text.delete("1.0", "end")

    c.execute("SELECT status, COUNT(*) FROM applications GROUP BY status")
    results = c.fetchall()
    analysis_text.insert("end", "📊 Applications by Status:\n\n")
    for status, count in results:
        analysis_text.insert("end", f"{status}: {count}\n")

    analysis_text.insert("end", "\n📈 Applications by Company:\n\n")
    c.execute("SELECT company, COUNT(*) FROM applications GROUP BY company")
    results = c.fetchall()
    for company, count in results:
        analysis_text.insert("end", f"{company}: {count}\n")

    conn.close()
