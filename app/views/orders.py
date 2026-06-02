import customtkinter as ctk
from tkinter import messagebox
import db.db as db

class OrdersView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Orders", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(top, text="+ Create Order", command=self.add_order_form).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_orders).pack(side="left", padx=4)

        self._sort_by = "`order_date`"
        self._sort_order = "DESC"

        self.sort_order_button = ctk.CTkComboBox(top, values=["DESC", "ASC"], width=90, command=self.set_sort_order)
        self.sort_order_button.set(self._sort_order)
        self.sort_order_button.pack(side="right", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_orders()

    def set_sort_order(self, sort_in_button_choice):
        self._sort_order = sort_in_button_choice
        self.load_orders()

    def load_orders(self):
        for widget in self.table.winfo_children():
            widget.destroy()

        try:
            # Invokes listOrderWithCustomerInfo internally map-bound to DictCursor format
            rows = db.get_orders()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not rows:
            ctk.CTkLabel(self.table, text="No orders found.").pack(pady=20)
            return

        headers = ["Order ID", "Customer Name", "Order Date", "Type", "Status", "Total Price"]
        widths = [80, 200, 150, 100, 120, 110]

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x", pady=2)

        for h, w in zip(headers, widths):
            ctk.CTkLabel(header, text=h, width=w, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            values = [
                row.get("order_id"),
                row.get("customer_name"),
                row.get("order_date"),
                row.get("order_type"),
                row.get("status"),
                f"{row.get('total_price'):,.2f}" if row.get("total_price") is not None else "0.00"
            ]

            for v, w in zip(values, widths):
                ctk.CTkLabel(line, text=str(v), width=w, anchor="w").pack(side="left", padx=5)

    def add_order_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Create New Order")
        form.geometry("360x300")
        form.grab_set()

        fields = ["Customer ID", "Order Date (YYYY-MM-DD)", "Order Type (IN_STORE/DELIVERY)"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(form, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(form, width=280)
            entry.pack()
            entries[field] = entry

        import datetime
        entries["Order Date (YYYY-MM-DD)"].insert(0, str(datetime.date.today()))

        def save():
            try:
                cust_id = int(entries["Customer ID"].get().strip())
                o_date = entries["Order Date (YYYY-MM-DD)"].get().strip()
                o_type = entries["Order Type (IN_STORE/DELIVERY)"].get().strip().upper()

                if not o_date or o_type not in ["IN_STORE", "DELIVERY"]:
                    raise ValueError("Type validation mismatch: Input must be 'IN_STORE' or 'DELIVERY'.")

                db.create_order(cust_id, o_date, o_type)
                form.destroy()
                self.load_orders()
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)