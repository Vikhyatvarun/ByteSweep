import os
import shutil
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import winsound
import subprocess

sound_path = os.path.join(os.path.dirname(__file__), "clean.wav")

def play_start_sound():
    winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

# ---- Delete Functions ---- #
def add_log(msg, tag="normal"):
    log_box.configure(state="normal")
    log_box.insert(tk.END, msg + "\n", tag)
    log_box.configure(state="disabled")
    log_box.see(tk.END)

def delete_folder(path):
    if os.path.exists(path):
        add_log(f"🗑️  Deleting: {path}", "info")
        try:
            shutil.rmtree(path, ignore_errors=True)
            add_log(f"✔️  Done: {path}", "success")
        except Exception as e:
            add_log(f"⚠️  Error deleting: {path} ({e})", "warning")
    else:
        add_log(f"⚠️  Not Found: {path}", "warning")


def delete_temp():
    delete_folder(os.environ.get("TEMP"))
    delete_folder(r"C:\Windows\Temp")


def delete_browser_cache():
    user = os.path.expanduser("~")

    CHROME_PATHS = [
        r"AppData\Local\Google\Chrome\User Data\Default\Cache",
        r"AppData\Local\Google\Chrome\User Data\Default\GPUCache",
        r"AppData\Local\Google\Chrome\User Data\Default\Code Cache",
        r"AppData\Local\Google\Chrome\User Data\ShaderCache",
        r"AppData\Local\Google\Chrome\User Data\Crashpad",
        r"AppData\Local\Google\Chrome\User Data\Default\Media Cache",
    ]

    EDGE_PATHS = [
        r"AppData\Local\Microsoft\Edge\User Data\Default\Cache",
        r"AppData\Local\Microsoft\Edge\User Data\Default\GPUCache",
        r"AppData\Local\Microsoft\Edge\User Data\Default\Code Cache",
        r"AppData\Local\Microsoft\Edge\User Data\ShaderCache",
    ]

    add_log("🌐 Cleaning Browser Cache…", "info")

    for rel_path in CHROME_PATHS + EDGE_PATHS:
        path = os.path.join(user, rel_path)
        try:
            shutil.rmtree(path, ignore_errors=True)
            add_log(f"🧹 Deleted: {path}", "success")
        except Exception as e:
            add_log(f"⚠️ Failed: {path} ({e})", "warning")

    add_log("✔️ Browser Cache Cleaned\n", "success")


def delete_prefetch():
    delete_folder(r"C:\Windows\Prefetch")


def delete_update_downloads():
    delete_folder(r"C:\Windows\SoftwareDistribution\Download")


def delete_thumbnails():
    folder = os.path.expanduser(r"~\AppData\Local\Microsoft\Windows\Explorer")
    add_log("🖼️ Deleting Thumbnails Cache…", "info")

    for file in os.listdir(folder):
        if file.startswith(("thumbcache_", "iconcache_")):
            try:
                os.remove(os.path.join(folder, file))
            except:
                pass

    add_log("✔️ Thumbnails Cache Cleaned", "success")


def delete_error_reports():
    delete_folder(r"C:\ProgramData\Microsoft\Windows\WER")


def empty_recycle_bin():
    add_log("♻️ Emptying Recycle Bin…", "info")

    subprocess.run(
        ["PowerShell", "Clear-RecycleBin", "-Force"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    add_log("✔️ Recycle Bin Emptied", "success")

# ---- Delete Selected ---- #
def delete_selected():
    play_start_sound()
    add_log("\n" + "="*41, "header")
    add_log("🚀  STARTING CLEANUP PROCESS", "header")
    add_log("="*41 + "\n", "header")
    
    if opt_temp.get(): delete_temp()
    if opt_browser_cache.get(): delete_browser_cache()
    if opt_prefetch.get(): delete_prefetch()
    if opt_update.get(): delete_update_downloads()
    if opt_thumbs.get(): delete_thumbnails()
    if opt_error.get(): delete_error_reports()
    if opt_recycle.get(): empty_recycle_bin()
    
    add_log("\n" + "="*41, "header")
    add_log("✅  CLEANUP COMPLETED SUCCESSFULLY", "header")
    add_log("="*41 + "\n", "header")

def select_all():
    for _, var in options:
        var.set(True)

def deselect_all():
    for _, var in options:
        var.set(False)

# ---- UI Window ---- #
root = tk.Tk()
root.title("ByteSweep - Windows Cleaner - by vikhyatvarun")
root.geometry("750x500")
root.resizable(False, False)
root.configure(bg="#1e1e2e")
icon_path = os.path.join(sys._MEIPASS, "logo.ico") if hasattr(sys, "_MEIPASS") else "logo.ico"
try:
    root.iconbitmap(icon_path)
except Exception:
    pass

# --- Modern Style Configuration --- #
style = ttk.Style()
style.theme_use("clam")

# Configure colors
bg_dark = "#1e1e2e"
bg_card = "#2b2b3c"
accent = "#89b4fa"
accent_hover = "#74c7ec"
text_color = "#cdd6f4"
success_color = "#a6e3a1"
warning_color = "#f9e2af"

style.configure("TFrame", background=bg_dark)
style.configure("Card.TFrame", background=bg_card, relief="flat")

style.configure("TLabel", 
                background=bg_dark, 
                foreground=text_color,
                font=("Segoe UI", 11))

style.configure("Title.TLabel",
                background=bg_dark,
                foreground=accent,
                font=("Segoe UI", 24, "bold"))

style.configure("Subtitle.TLabel",
                background=bg_dark,
                foreground=text_color,
                font=("Segoe UI", 10))

style.configure("Modern.TCheckbutton",
                background=bg_card,
                foreground=text_color,
                font=("Segoe UI", 11),
                borderwidth=0,
                indicatorcolor="#89b4fa",
                indicatorrelief="flat")
style.map("Modern.TCheckbutton",
          background=[("active", bg_card)],
          foreground=[("active", accent)],
          indicatorcolor=[("selected", accent), ("!selected", "#45475a")])

style.configure("Accent.TButton",
                background=accent,
                foreground="#1e1e2e",
                font=("Segoe UI", 12, "bold"),
                borderwidth=0,
                focuscolor="none")
style.map("Accent.TButton",
          background=[("active", accent_hover)])

style.configure("Secondary.TButton",
                background=bg_card,
                foreground=text_color,
                font=("Segoe UI", 10),
                borderwidth=0,
                focuscolor="none")
style.map("Secondary.TButton",
          background=[("active", "#3b3b4c")])

# ---- HEADER ---- #
header_frame = ttk.Frame(root, style="TFrame")
header_frame.pack(fill="x", padx=30, pady=(5, 10))

title_label = ttk.Label(header_frame, text="🧹 ByteSweep" , style="Title.TLabel")
title_label.pack(anchor="w")

subtitle_label = ttk.Label(header_frame, 
                          text="Clean up temporary files and free up disk space", 
                          style="Subtitle.TLabel")
subtitle_label.pack(anchor="w", pady=(5, 0))

# ---- MAIN CONTENT ---- #
content_frame = ttk.Frame(root, style="TFrame")
content_frame.pack(fill="both", expand=True, padx=30, pady=10)

# ---- LEFT: Log Panel ---- #
left_panel = ttk.Frame(content_frame, style="Card.TFrame")
left_panel.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=(0, 10))

log_title = ttk.Label(left_panel,
                     text="Activity Log:",
                     background=bg_card,
                     foreground=accent,
                     font=("Segoe UI", 13, "bold"))
log_title.pack(anchor="w", padx=20, pady=(20, 10))

log_box = scrolledtext.ScrolledText(left_panel,
                                   width=45,
                                   height=18,
                                   font=("Cascadia Code", 9),
                                   bg="#181825",
                                   fg=text_color,
                                   insertbackground=accent,
                                   relief="flat",
                                   borderwidth=0,
                                   padx=10,
                                   pady=10)
log_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
log_box.configure(state="disabled")

# Configure log tags for colored output
log_box.tag_configure("header", foreground=accent, font=("Cascadia Code", 10, "bold"))
log_box.tag_configure("success", foreground=success_color)
log_box.tag_configure("warning", foreground=warning_color)
log_box.tag_configure("info", foreground=text_color)

# ---- RIGHT: Options Panel ---- #
right_panel = ttk.Frame(content_frame, style="Card.TFrame")
right_panel.pack(side="left", fill="both", padx=0, pady=(0, 10))

options_title = ttk.Label(right_panel, 
                         text="Select items to clean:", 
                         background=bg_card,
                         foreground=accent,
                         font=("Segoe UI", 13, "bold"))
options_title.pack(anchor="w", padx=20, pady=(15, 10))

opt_temp = tk.BooleanVar(value=True)
opt_browser_cache = tk.BooleanVar(value=True)
opt_win_temp = tk.BooleanVar(value=True)
opt_prefetch = tk.BooleanVar(value=True)
opt_update = tk.BooleanVar(value=True)
opt_thumbs = tk.BooleanVar(value=True)
opt_error = tk.BooleanVar(value=True)
opt_recycle = tk.BooleanVar(value=True)

options = [
    ("📁 User Temp Folder", opt_temp),
    ("🌐 Browser Cache", opt_browser_cache),
    ("⚡ Prefetch Files", opt_prefetch),
    ("📦 Windows Update Cache", opt_update),
    ("🎨 Thumbnails Cache", opt_thumbs),
    ("⚠️ Error Reports", opt_error),
    ("♻️ Recycle Bin", opt_recycle),
]

for text, var in options:
    cb = tk.Checkbutton(right_panel, 
                       text=text, 
                       variable=var,
                       bg=bg_card,
                       fg=text_color,
                       activebackground=bg_card,
                       activeforeground=accent,
                       selectcolor=bg_card,
                       font=("Segoe UI", 11),
                       relief="flat",
                       borderwidth=0,
                       highlightthickness=0,
                       cursor="hand2")
    cb.pack(anchor="w", padx=20, pady=3)

# Button container
button_container = ttk.Frame(right_panel, style="Card.TFrame")
button_container.pack(fill="x", padx=20, pady=(10, 10))

select_all_btn = ttk.Button(button_container, 
                            text="Select All", 
                            command=select_all,
                            style="Secondary.TButton")
select_all_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

deselect_all_btn = ttk.Button(button_container, 
                              text="Deselect All", 
                              command=deselect_all,
                              style="Secondary.TButton")
deselect_all_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

# Main action button
delete_btn_frame = ttk.Frame(right_panel, style="Card.TFrame")
delete_btn_frame.pack(fill="x", padx=20, pady=(5, 15))

delete_btn = ttk.Button(delete_btn_frame, 
                       text="🚀 START CLEANUP", 
                       command=delete_selected,
                       style="Accent.TButton")
delete_btn.pack(fill="x", ipady=8)

# Initial welcome message
add_log("👋 Welcome to ByteSweep!", "header")
add_log("Select the items you want to clean and click 'START CLEANING'.\n", "info")

root.mainloop()