"""
Memory Segmentation Simulator
Stage 2 GUI prototype (Tkinter) + Stage 3 access-protection extension.

Checks performed before a physical address is produced:
  1. The segment number must exist.
  2. 0 <= offset < limit.
  3. The requested operation must be permitted for the segment.

Physical Address = Base Address + Offset
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Segment table: segment number -> name, base address, limit, permissions
segments = {
    0: {"name": "Code",  "base": 1000, "limit": 400, "permissions": ["read", "execute"]},
    1: {"name": "Data",  "base": 2000, "limit": 300, "permissions": ["read", "write"]},
    2: {"name": "Stack", "base": 3000, "limit": 200, "permissions": ["read", "write"]},
    3: {"name": "Heap",  "base": 4000, "limit": 500, "permissions": ["read", "write"]},
}

OPERATIONS = ["Read", "Write", "Execute"]


def translate(segment_no, offset, access_type):
    """Core logic. Returns (ok, message, details_dict_or_None)."""
    if segment_no not in segments:
        return False, "Invalid address: Segment does not exist.", None

    seg = segments[segment_no]
    base, limit = seg["base"], seg["limit"]

    if offset < 0 or offset >= limit:
        return False, f"Invalid address! Offset must be from 0 to {limit - 1}.", None

    if access_type.lower() not in seg["permissions"]:
        allowed = ", ".join(p.capitalize() for p in seg["permissions"])
        return (False,
                f"Access denied: {access_type.capitalize()} is not permitted "
                f"on {seg['name']} segment.\nAllowed: {allowed}",
                None)

    physical = base + offset
    msg = (f"Valid Address\nSegment: {seg['name']}\n"
           f"Operation: {access_type.capitalize()} (permitted)\n"
           f"Base = {base}, Offset = {offset}\n"
           f"Physical Address = {base} + {offset} = {physical}")
    return True, msg, {"physical": physical}


# ----------------------------- GUI callbacks -----------------------------
def translate_address():
    try:
        segment_no = int(segment_entry.get())
        offset = int(offset_entry.get())
    except ValueError:
        messagebox.showerror("Input Error",
                             "Enter whole numbers for segment number and offset.")
        return

    ok, message, _ = translate(segment_no, offset, operation_var.get())
    result_label.config(text=message, foreground="green" if ok else "red")


def clear_fields():
    segment_entry.delete(0, tk.END)
    offset_entry.delete(0, tk.END)
    operation_var.set(OPERATIONS[0])
    result_label.config(text="", foreground="black")


# ------------------------------- GUI layout -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Memory Segmentation Simulator")
    root.geometry("620x620")

    ttk.Label(root, text="MEMORY SEGMENTATION SIMULATOR",
              font=("Calibri", 15, "bold")).pack(pady=(12, 0))
    ttk.Label(root, text="Logical-to-Physical Address Translation "
                         "with Access Protection").pack(pady=(0, 10))

    # Segment table
    table = ttk.Treeview(root,
                         columns=("no", "name", "base", "limit", "perm"),
                         show="headings", height=4)
    for col, head, w in zip(("no", "name", "base", "limit", "perm"),
                            ("Segment No.", "Name", "Base", "Limit",
                             "Permitted Operations"),
                            (90, 80, 80, 80, 180)):
        table.heading(col, text=head)
        table.column(col, width=w, anchor="center")
    for no, s in segments.items():
        table.insert("", tk.END,
                     values=(no, s["name"], s["base"], s["limit"],
                             ", ".join(p.capitalize() for p in s["permissions"])))
    table.pack(padx=20, pady=8)

    # Logical address input
    form = ttk.LabelFrame(root, text="Logical Address Input")
    form.pack(padx=20, pady=8, fill="x")

    ttk.Label(form, text="Segment Number").grid(row=0, column=0, padx=10, pady=6, sticky="w")
    segment_entry = ttk.Entry(form, width=15)
    segment_entry.grid(row=0, column=1, padx=10, pady=6)

    ttk.Label(form, text="Offset").grid(row=1, column=0, padx=10, pady=6, sticky="w")
    offset_entry = ttk.Entry(form, width=15)
    offset_entry.grid(row=1, column=1, padx=10, pady=6)

    ttk.Label(form, text="Operation").grid(row=2, column=0, padx=10, pady=6, sticky="w")
    operation_var = tk.StringVar(value=OPERATIONS[0])
    operation_box = ttk.Combobox(form, textvariable=operation_var,
                                 values=OPERATIONS, state="readonly", width=12)
    operation_box.grid(row=2, column=1, padx=10, pady=6)

    # Buttons
    buttons = ttk.Frame(root)
    buttons.pack(pady=8)
    ttk.Button(buttons, text="Translate Address",
               command=translate_address).grid(row=0, column=0, padx=6)
    ttk.Button(buttons, text="Clear",
               command=clear_fields).grid(row=0, column=1, padx=6)

    # Result
    result_label = ttk.Label(root, text="", font=("Calibri", 12), justify="left")
    result_label.pack(padx=20, pady=10, anchor="w")

    root.mainloop()
