import tkinter as tk
from tkinter import ttk
import time

BUTTON_LABELS = {1: "Left", 2: "Middle", 3: "Right", 4: "Back", 5: "Forward"}

counts = {"total": 0, "double": 0}
last_click = {"button": None, "time": 0}


def get_threshold():
    try:
        ms = max(10, min(1000, int(delay_entry.get())))
        return ms / 1000
    except ValueError:
        return 0.1


def on_press(event):
    btn = event.num
    name = BUTTON_LABELS.get(btn, f"Button {btn}")
    now = time.time()

    is_double = (
        last_click["button"] == btn and now - last_click["time"] < get_threshold()
    )
    last_click["button"] = btn
    last_click["time"] = now

    counts["total"] += 1
    if is_double:
        counts["double"] += 1

    label = "double click" if is_double else "click"
    last_var.set(f"{label}  —  {name}")
    total_var.set(counts["total"])
    double_var.set(counts["double"])

    for w in (target_frame, lbl1, lbl2):
        w.configure(bg="lightyellow")
    root.after(
        120, lambda: [w.configure(bg=DEFAULT_BG) for w in (target_frame, lbl1, lbl2)]
    )

    ms = int((now % 1) * 1000)
    log_list.insert(0, f"{time.strftime('%H:%M:%S')}.{ms:03d}  {label:<14}  {name}")
    if log_list.size() > 60:
        log_list.delete(60, tk.END)


def reset():
    counts["total"] = counts["double"] = 0
    last_var.set("Waiting for input...")
    total_var.set(0)
    double_var.set(0)


def clear_log():
    log_list.delete(0, tk.END)


root = tk.Tk()
root.title("Mouse Button Tester")
root.geometry("500x480")

DEFAULT_BG = root.cget("bg")

last_var = tk.StringVar(value="Waiting for input...")
total_var = tk.IntVar(value=0)
double_var = tk.IntVar(value=0)

# Click target
target_frame = tk.Frame(root, height=120, cursor="hand2", relief="solid", bd=1)
target_frame.pack(fill="x", padx=16, pady=(16, 8))
target_frame.pack_propagate(False)
lbl1 = tk.Label(target_frame, textvariable=last_var, font=("", 15))
lbl1.pack(expand=True)
lbl2 = tk.Label(target_frame, text="Click anywhere in this box with any mouse button")
lbl2.pack(pady=(0, 10))
for lbl in (lbl1, lbl2):
    lbl.bindtags((target_frame, "Label", root, "all"))
target_frame.bind("<ButtonPress>", on_press)

# Threshold setting
delay_frame = ttk.Frame(root)
delay_frame.pack(fill="x", padx=16, pady=(0, 8))
ttk.Label(delay_frame, text="Double-click threshold (10–1000 ms):").pack(side="left")
delay_entry = ttk.Entry(delay_frame, width=6)
delay_entry.insert(0, "100")
delay_entry.pack(side="left", padx=(8, 4))
ttk.Label(delay_frame, text="ms").pack(side="left")

# Counters
grid_frame = ttk.Frame(root)
grid_frame.pack(fill="x", padx=16, pady=4)
for i, (lbl, var) in enumerate(
    [("Total clicks", total_var), ("Double clicks", double_var)]
):
    cell = ttk.LabelFrame(grid_frame, text=lbl)
    cell.grid(row=0, column=i, padx=4, pady=4, sticky="nsew")
    grid_frame.columnconfigure(i, weight=1)
    ttk.Label(cell, textvariable=var, font=("", 20, "bold")).pack(pady=6)

# Buttons
btn_frame = ttk.Frame(root)
btn_frame.pack(fill="x", padx=16, pady=(6, 4))
ttk.Button(btn_frame, text="Reset stats", command=reset).pack(side="left", padx=(0, 6))
ttk.Button(btn_frame, text="Clear log", command=clear_log).pack(side="left")

# Log
log_frame = ttk.Frame(root)
log_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))
scrollbar = ttk.Scrollbar(log_frame)
scrollbar.pack(side="right", fill="y")
log_list = tk.Listbox(
    log_frame,
    yscrollcommand=scrollbar.set,
    font=("Courier", 11),
    relief="flat",
    bd=1,
    activestyle="none",
)
log_list.pack(fill="both", expand=True)
scrollbar.config(command=log_list.yview)

root.mainloop()
