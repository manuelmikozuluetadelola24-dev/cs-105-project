import customtkinter as ctk
from tkinter import messagebox
import db.db as db


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tip = ctk.CTkToplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        ctk.CTkLabel(self.tip, text=self.text, fg_color="#333333", text_color="white", corner_radius=6).pack(padx=6, pady=4)

    def hide(self, event):
        if self.tip:
            self.tip.destroy()
            self.tip = None
class SuppliersView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Suppliers", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(top, text="+ Add Supplier", command=self.add_supplier_form).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_suppliers).pack(side="left", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_suppliers()

    def load_suppliers(self):
        for widget in self.table.winfo_children():
            widget.destroy()

        try:
            rows = db.get_suppliers()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not rows:
            ctk.CTkLabel(self.table, text="No suppliers found.").pack(pady=20)
            return

        headers = ["ID", "Name", "Contact", "Street", "Barangay", "City", "Province"]
        widths =   [50,   180,    120,       150,      120,        120,    120]
        max_chars = [6,   22,     13,        18,       16,         14,     14]

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x")
        for h, w in zip(headers, widths):
            ctk.CTkLabel(header, text=h, width=w, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            values = [
                row.get("supplier_id"),
                row.get("supplier_name"),
                row.get("contact_number"),
                row.get("supplier_street"),
                row.get("supplier_barangay"),
                row.get("supplier_city"),
                row.get("supplier_province"),
            ]

            for v, w, m in zip(values, widths, max_chars):
                text = str(v)
                truncated = text[:m - 1] + "…" if len(text) > m else text
                label = ctk.CTkLabel(line, text=truncated, width=w, anchor="w")
                label.pack(side="left", padx=5)
                if len(text) > m:
                    Tooltip(label, text)

    def add_supplier_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Add Supplier")
        form.geometry("360x400")
        form.grab_set()

        fields = ["Supplier Name", "Contact Number", "Street", "Barangay", "City", "Province"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(form, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(form, width=280)
            entry.pack()
            entries[field] = entry

        def save():
            try:
                name    = entries["Supplier Name"].get().strip()
                contact = entries["Contact Number"].get().strip()
                street  = entries["Street"].get().strip()
                barangay = entries["Barangay"].get().strip()
                city    = entries["City"].get().strip()
                province = entries["Province"].get().strip()

                if not name or not contact:
                    raise ValueError("Supplier name and contact number are required.")

                db.add_supplier(name, contact, street, barangay, city, province)
                form.destroy()
                self.load_suppliers()

            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)