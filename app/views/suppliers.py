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

        self.search_entry = ctk.CTkEntry(top, placeholder_text="Search name/city/contact", width=250)
        self.search_entry.pack(side="left", padx=(0, 8))

        ctk.CTkButton(top, text="Search", command=self.search).pack(side="left", padx=4)
        ctk.CTkButton(top, text="+ Add Supplier", command=self.add_supplier_form).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_suppliers).pack(side="left", padx=4)

        self._sort_by = "supplier_id"
        self._sort_order = "DESC"

        self.sort_order_button = ctk.CTkComboBox(top, values=["DESC", "ASC"], width=90, command=self.set_sort_order)
        self.sort_order_button.set(self._sort_order)
        self.sort_order_button.pack(side="right", padx=4)

        self.sort_by_button = ctk.CTkComboBox(
            top,
            values=["supplier_id", "supplier_name", "supplier_city"],
            width=150,
            command=self.set_sort_by
        )
        self.sort_by_button.set(self._sort_by)
        self.sort_by_button.pack(side="right", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_suppliers()

    _NUMERIC_COLS = {"supplier_id"}

    def _sort_key(self, row):
        val = row.get(self._sort_by)
        if self._sort_by in self._NUMERIC_COLS:
            try:
                return (0, int(val))
            except (TypeError, ValueError):
                return (1, 0)
        return (0, str(val or "").lower())

    def set_sort_by(self, choice):
        self._sort_by = choice
        self.load_suppliers()

    def set_sort_order(self, choice):
        self._sort_order = choice
        self.load_suppliers()

    def build_table(self, rows):
        for widget in self.table.winfo_children():
            widget.destroy()

        if not rows:
            ctk.CTkLabel(self.table, text="No suppliers found.").pack(pady=20)
            return

        headers  = ["ID", "Name",  "Contact", "Street", "Barangay", "City", "Province"]
        widths   = [50,   180,     120,        150,      120,        120,    120]
        max_chars = [6,   22,      13,         18,       16,         14,     14]

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

    def load_suppliers(self):
        try:
            rows = db.get_suppliers()
            # Sort in Python since get_suppliers doesn't take order args
            reverse = self._sort_order == "DESC"
            rows = sorted(rows, key=self._sort_key, reverse=reverse)
            self.build_table(rows)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search(self):
        term = self.search_entry.get().strip().lower()
        if not term:
            self.load_suppliers()
            return

        try:
            rows = db.get_suppliers()
            filtered = [
                r for r in rows
                if term in str(r.get("supplier_name", "")).lower()
                or term in str(r.get("contact_number", "")).lower()
                or term in str(r.get("supplier_city", "")).lower()
                or term in str(r.get("supplier_barangay", "")).lower()
            ]
            reverse = self._sort_order == "DESC"
            filtered = sorted(filtered, key=self._sort_key, reverse=reverse)
            self.build_table(filtered)
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
                name     = entries["Supplier Name"].get().strip()
                contact  = entries["Contact Number"].get().strip()
                street   = entries["Street"].get().strip()
                barangay = entries["Barangay"].get().strip()
                city     = entries["City"].get().strip()
                province = entries["Province"].get().strip()

                if not name or not contact:
                    raise ValueError("Supplier name and contact number are required.")

                db.add_supplier(name, contact, street, barangay, city, province)
                form.destroy()
                self.load_suppliers()

            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)