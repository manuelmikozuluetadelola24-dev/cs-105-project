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
class ProductsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Products", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        self.search_entry = ctk.CTkEntry(top, placeholder_text="Search product/category", width=250)
        self.search_entry.pack(side="left", padx=(0, 8))

        ctk.CTkButton(top, text="Search", command=self.search).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_products).pack(side="left", padx=4)
        ctk.CTkButton(top, text="+ Add Product", command=self.add_product_form).pack(side="left", padx=4)

        self._sort_by = "`product_id`"
        self._sort_order = "DESC"

        self.sort_order_button = ctk.CTkComboBox(top, values=["DESC", "ASC"], width=90, command=self.set_sort_order)
        self.sort_order_button.set(self._sort_order)
        self.sort_order_button.pack(side="right", padx=4)

        self.sort_by_button = ctk.CTkComboBox(
            top, 
            values=["`product_id`", "`product_name`", "`price`", "`stock_quantity`", "`category_id`"], 
            width=150, 
            command=self.set_sort_by
        )
        self.sort_by_button.set(self._sort_by)
        self.sort_by_button.pack(side="right", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_products()

    def set_sort_by(self, sort_by_button_choice):
        self._sort_by = sort_by_button_choice
        self.load_products()

    def set_sort_order(self, sort_in_button_choice):
        self._sort_order = sort_in_button_choice
        self.load_products()

    def clear_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()

    def build_table(self, rows):
        self.clear_table()

        headers = ["ID", "Product", "Category", "Price", "Stock"]
        widths = [70, 220, 160, 100, 100]

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x", pady=2)

        for h, w in zip(headers, widths):
            ctk.CTkLabel(header, text=h, width=w, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            values = [
                row.get("product_id"),
                row.get("product_name"),
                row.get("category_name"),
                row.get("price"),
                row.get("stock_quantity"),
            ]

            max_chars = [10, 28, 20, 10, 10]

            for v, w, m in zip(values, widths, max_chars):
                text = str(v)
                truncated = f"{text[:m - 1]}…" if len(text) > m else text
                label = ctk.CTkLabel(line, text=truncated, width=w, anchor="w")
                label.pack(side="left", padx=5)
                if len(text) > m:
                    Tooltip(label, text)

    def load_products(self):
        try:
            self.build_table(db.get_products(order=self._sort_order, order_by=self._sort_by))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search(self):
        term = self.search_entry.get().strip()
        if not term:
            self.load_products()
            return

        try:
            self.build_table(db.search_products(term))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_product_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Add Product")
        form.geometry("360x330")
        form.grab_set()

        fields = ["Product Name", "Category ID", "Price", "Stock Quantity"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(form, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(form, width=280)
            entry.pack()
            entries[field] = entry

        def save():
            try:
                name = entries["Product Name"].get().strip()
                category_id = int(entries["Category ID"].get())
                price = float(entries["Price"].get())
                stock = int(entries["Stock Quantity"].get())

                if not name or price <= 0 or stock < 0:
                    raise ValueError("Invalid product data.")

                db.add_product(name, category_id, price, stock)
                form.destroy()
                self.load_products()

            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)