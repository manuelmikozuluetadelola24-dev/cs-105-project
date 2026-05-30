import customtkinter as ctk
from tkinter import messagebox
import db.db as db


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

        columns = list(rows[0].keys())

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x")

        for col in columns:
            ctk.CTkLabel(header, text=col, width=150, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            for col in columns:
                ctk.CTkLabel(line, text=str(row.get(col)), width=150, anchor="w").pack(side="left", padx=5)

    def add_supplier_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Add Supplier")
        form.geometry("360x260")
        form.grab_set()

        fields = ["Supplier Name", "Contact Number", "Address"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(form, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(form, width=280)
            entry.pack()
            entries[field] = entry

        def save():
            try:
                name = entries["Supplier Name"].get().strip()
                contact = entries["Contact Number"].get().strip()
                address = entries["Address"].get().strip()

                if not name or not contact:
                    raise ValueError("Supplier name and contact number are required.")

                db.add_supplier(name, contact, address)
                form.destroy()
                self.load_suppliers()

            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)