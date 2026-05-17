import os, sys
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk

LOCK_FILE = "app_instance.lock"

def ensure_single_instance():
    """Prevents multiple instances of the app from running."""
    if os.path.exists(LOCK_FILE):
        from tkinter import Tk
        root = Tk()
        root.withdraw()
        messagebox.showerror("Already Running",
            "⚠️ The Job Application Tracker is already running.\n\nPlease close the existing window first.")
        sys.exit(0)
    else:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

def cleanup_lock():
    """Removes the lock file on exit."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def meme_popup(title, message, meme_path="assets/Back_to_the_future.jpg", master=None):
    """Displays a fun meme popup with a custom message and image."""
    import os

    # --- Resolve image path relative to script directory ---
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    meme_full_path = os.path.join(base_dir, meme_path)

    # --- Create popup window ---
    popup = ttk.Toplevel(master)
    popup.title(title)
    popup.geometry("300x350")
    popup.resizable(False, False)
    popup.configure(bg="#2b2b2b")

    # --- Center popup on screen ---
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (400 // 2)
    y = (popup.winfo_screenheight() // 2) - (400 // 2)
    popup.geometry(f"+{x}+{y}")

    # --- Keep it on top ---
    popup.transient(master)
    popup.grab_set()
    popup.focus_force()

    # --- Image handling ---
    try:
        if not os.path.exists(meme_full_path):
            raise FileNotFoundError

        img = Image.open(meme_full_path)
        img = img.resize((225, 225), Image.LANCZOS)
        meme_img = ImageTk.PhotoImage(img)

        meme_label = ttk.Label(popup, image=meme_img)
        meme_label.image = meme_img  # prevent garbage collection
        meme_label.pack(pady=(15, 10))
    except Exception as e:
        ttk.Label(popup, text="(Meme not found 😢)", bootstyle="light").pack(pady=20)

    # --- Message and button ---
    ttk.Label(
        popup,
        text=message,
        bootstyle="inverse-dark",
        wraplength=350,
        anchor="center",
        justify="center"
    ).pack(pady=(10, 10))

    ttk.Button(popup, text="OK", command=popup.destroy, bootstyle="success").pack(pady=(5, 15))
