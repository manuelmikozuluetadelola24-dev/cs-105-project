import customtkinter as ctk
from tkinter import messagebox
import datetime
import db.db as db

class OrdersView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Orders", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        self.search_entry = ctk.CTkEntry(top, placeholder_text="Search customer/status/type", width=250)
        self.search_entry.pack(side="left", padx=(0, 8))

        ctk.CTkButton(top, text="Search", command=self.search).pack(side="left", padx=4)
        ctk.CTkButton(top, text="+ Create Order", command=self.add_order_form).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_orders).pack(side="left", padx=4)

        self._sort_by = "`order_date`"
        self._sort_order = "DESC"

        self.sort_order_button = ctk.CTkComboBox(top, values=["DESC", "ASC"], width=90, command=self.set_sort_order)
        self.sort_order_button.set(self._sort_order)
        self.sort_order_button.pack(side="right", padx=4)

        self.sort_by_button = ctk.CTkComboBox(
            top,
            values=["`order_date`", "`order_id`", "`customer_name`", "`status`"],
            width=160,
            command=self.set_sort_by
        )
        self.sort_by_button.set(self._sort_by)
        self.sort_by_button.pack(side="right", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_orders()

    def set_sort_by(self, choice):
        self._sort_by = choice
        self.load_orders()

    def set_sort_order(self, choice):
        self._sort_order = choice
        self.load_orders()

    def build_table(self, rows):
        for widget in self.table.winfo_children():
            widget.destroy()

        if not rows:
            ctk.CTkLabel(self.table, text="No orders found.").pack(pady=20)
            return

        headers = ["Order ID", "Customer Name", "Order Date", "Type", "Status", "Total Price", "", ""]
        widths   = [70,        180,              110,          90,     110,      100,           110, 120]

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x", pady=2)
        for h, w in zip(headers, widths):
            ctk.CTkLabel(header, text=h, width=w, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            order_id = row.get("order_id")
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            values = [
                order_id,
                row.get("customer_name"),
                row.get("order_date"),
                row.get("order_type"),
                row.get("status"),
                f"{row.get('total_price'):,.2f}" if row.get("total_price") is not None else "0.00",
            ]
            for v, w in zip(values, widths):
                ctk.CTkLabel(line, text=str(v), width=w, anchor="w").pack(side="left", padx=5)

            ctk.CTkButton(
                line, text="View Items", width=100,
                command=lambda oid=order_id: self.open_items_window(oid)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                line, text="Update Status", width=110,
                command=lambda oid=order_id, cur=row.get("status"): self.open_status_window(oid, cur)
            ).pack(side="left", padx=4)

    def load_orders(self):
        try:
            rows = db.listOrderWithCustomerInfo(order=self._sort_order, order_by=self._sort_by)
            self.build_table(rows)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search(self):
        term = self.search_entry.get().strip().lower()
        if not term:
            self.load_orders()
            return

        try:
            rows = db.listOrderWithCustomerInfo(order=self._sort_order, order_by=self._sort_by)
            filtered = [
                r for r in rows
                if term in str(r.get("customer_name", "")).lower()
                or term in str(r.get("status", "")).lower()
                or term in str(r.get("order_type", "")).lower()
            ]
            self.build_table(filtered)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Order Items sub-window
    def open_items_window(self, order_id):
        win = ctk.CTkToplevel(self)
        win.title(f"Order #{order_id} — Items")
        win.geometry("620x420")
        win.grab_set()

        ctk.CTkLabel(win, text=f"Items in Order #{order_id}", font=("Arial", 16, "bold")).pack(anchor="w", padx=16, pady=(12, 4))

        ctk.CTkButton(win, text="+ Add Item", command=lambda: self.open_add_item_form(order_id, win)).pack(anchor="w", padx=16, pady=(0, 8))

        list_frame_container = ctk.CTkFrame(win, fg_color="transparent")
        list_frame_container.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        def refresh_items():
            for w in list_frame_container.winfo_children():
                w.destroy()

            col_frame = ctk.CTkScrollableFrame(list_frame_container, fg_color="white")
            col_frame.pack(fill="both", expand=True)

            headers = ["Item ID", "Product", "Qty", "Unit Price", "Subtotal"]
            widths   = [70,        200,        60,    100,          100]

            hdr = ctk.CTkFrame(col_frame, fg_color="#e5e7eb")
            hdr.pack(fill="x")
            for h, w in zip(headers, widths):
                ctk.CTkLabel(hdr, text=h, width=w, anchor="w", font=("Arial", 11, "bold")).pack(side="left", padx=4)

            try:
                items = db.listOrderItemsInOrder(with_id=order_id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return

            if not items:
                ctk.CTkLabel(col_frame, text="No items yet.").pack(pady=10)
                return

            for item in items:
                r = ctk.CTkFrame(col_frame, fg_color="transparent")
                r.pack(fill="x", pady=1)
                row_vals = [
                    item.get("order_item_id"),
                    item.get("product_name"),
                    item.get("quantity"),
                    f"{item.get('selling_price'):,.2f}",
                    f"{item.get('item_total'):,.2f}",
                ]
                for v, w in zip(row_vals, widths):
                    ctk.CTkLabel(r, text=str(v), width=w, anchor="w").pack(side="left", padx=4)

        win._refresh_items = refresh_items
        refresh_items()

    # Add Order Item form
    def open_add_item_form(self, order_id, parent_win):
        form = ctk.CTkToplevel(parent_win)
        form.title("Add Item to Order")
        form.geometry("380x340")
        form.grab_set()

        try:
            products = db.get_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            form.destroy()
            return

        product_map = {f"{p['product_name']} (#{p['product_id']}) — stock: {p['stock_quantity']}": p for p in products}
        product_labels = list(product_map.keys())

        ctk.CTkLabel(form, text="Product").pack(pady=(14, 0))
        product_combo = ctk.CTkComboBox(form, values=product_labels, width=320)
        product_combo.pack()
        if product_labels:
            product_combo.set(product_labels[0])

        ctk.CTkLabel(form, text="Quantity").pack(pady=(10, 0))
        qty_entry = ctk.CTkEntry(form, width=320)
        qty_entry.pack()
        qty_entry.insert(0, "1")

        ctk.CTkLabel(form, text="Selling Price").pack(pady=(10, 0))
        price_entry = ctk.CTkEntry(form, width=320)
        price_entry.pack()

        def on_product_select(choice):
            p = product_map.get(choice)
            if p:
                price_entry.delete(0, "end")
                price_entry.insert(0, str(p.get("price", "")))

        product_combo.configure(command=on_product_select)
        on_product_select(product_combo.get())

        def save():
            try:
                chosen = product_combo.get()
                p = product_map.get(chosen)
                if not p:
                    raise ValueError("Please select a valid product.")
                product_id = p["product_id"]
                quantity   = int(qty_entry.get().strip())
                price      = float(price_entry.get().strip())
                if quantity <= 0 or price <= 0:
                    raise ValueError("Quantity and price must be positive.")
                db.add_order_item(order_id, product_id, quantity, price)
                form.destroy()
                parent_win._refresh_items()
                self.load_orders()
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Add Item", command=save).pack(pady=16)

    # Update Status window
    def open_status_window(self, order_id, current_status):
        win = ctk.CTkToplevel(self)
        win.title(f"Update Order #{order_id} Status")
        win.geometry("320x260")
        win.grab_set()

        ctk.CTkLabel(win, text=f"Order #{order_id}", font=("Arial", 14, "bold")).pack(pady=(16, 4))
        ctk.CTkLabel(win, text=f"Current status: {current_status}").pack(pady=(0, 12))

        is_locked = (current_status or "").upper() in ["DELIVERED", "CANCELLED"]

        if is_locked:
            ctk.CTkLabel(
                win,
                text="This order is locked.\nNo further changes allowed.",
                text_color="gray",
                justify="center",
            ).pack(pady=(0, 12))
            ctk.CTkButton(win, text="Close", command=win.destroy).pack(pady=8)
            return

        status_combo = ctk.CTkComboBox(win, values=["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"], width=240)
        status_combo.set(current_status or "PENDING")
        status_combo.pack(pady=10)

        def save():
            new_status = status_combo.get()
            try:
                db.update_order_status(order_id, new_status)
                win.destroy()
                self.load_orders()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(win, text="Save Status", command=save).pack(pady=16)

    # Create Order form
    def add_order_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Create New Order")
        form.geometry("400x360")
        form.grab_set()

        ctk.CTkLabel(form, text="Search Customer Name").pack(pady=(14, 0))
        search_entry = ctk.CTkEntry(form, width=320, placeholder_text="Type to search…")
        search_entry.pack()

        customer_combo = ctk.CTkComboBox(form, values=[], width=320)
        customer_combo.pack(pady=(4, 0))

        self._customer_map = {}

        def search_customers(*_):
            term = search_entry.get().strip()
            try:
                results = db.search_customers(term) if term else db.get_customers()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return
            self._customer_map = {
                f"{c['customer_name']} (#{c['customer_id']})": c["customer_id"]
                for c in results
            }
            labels = list(self._customer_map.keys())
            customer_combo.configure(values=labels)
            if labels:
                customer_combo.set(labels[0])
            else:
                customer_combo.set("")

        ctk.CTkButton(form, text="Search", command=search_customers).pack(pady=(6, 0))
        search_customers()

        ctk.CTkLabel(form, text="Order Date (YYYY-MM-DD)").pack(pady=(12, 0))
        date_entry = ctk.CTkEntry(form, width=320)
        date_entry.pack()
        date_entry.insert(0, str(datetime.date.today()))

        ctk.CTkLabel(form, text="Order Type").pack(pady=(10, 0))
        type_combo = ctk.CTkComboBox(form, values=["IN_STORE", "DELIVERY"], width=320)
        type_combo.set("IN_STORE")
        type_combo.pack()

        def save():
            try:
                chosen = customer_combo.get()
                cust_id = self._customer_map.get(chosen)
                if not cust_id:
                    raise ValueError("Please select a valid customer.")
                o_date  = date_entry.get().strip()
                o_type  = type_combo.get()
                if not o_date:
                    raise ValueError("Order date is required.")
                db.create_order(cust_id, o_date, o_type)
                form.destroy()
                self.load_orders()
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=16)