import customtkinter as ctk
from tkinter import messagebox
import db.db as db


class ShipmentView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Shipments", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        self.search_entry = ctk.CTkEntry(top, placeholder_text="Search supplier/reference/status", width=250)
        self.search_entry.pack(side="left", padx=(0, 8))

        ctk.CTkButton(top, text="Search", command=self.search).pack(side="left", padx=4)
        ctk.CTkButton(top, text="+ Log Shipment", command=self.add_shipment_form).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_shipments).pack(side="left", padx=4)

        self._sort_by = "shipment_id"
        self._sort_order = "DESC"

        self.sort_order_button = ctk.CTkComboBox(top, values=["DESC", "ASC"], width=90, command=self.set_sort_order)
        self.sort_order_button.set(self._sort_order)
        self.sort_order_button.pack(side="right", padx=4)

        self.sort_by_button = ctk.CTkComboBox(
            top,
            values=["shipment_id", "supplier_name", "shipment_date", "status"],
            width=160,
            command=self.set_sort_by
        )
        self.sort_by_button.set(self._sort_by)
        self.sort_by_button.pack(side="right", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_shipments()

    # Numeric columns that must be sorted as int, not string
    _NUMERIC_COLS = {"shipment_id", "supplier_id"}

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
        self.load_shipments()

    def set_sort_order(self, choice):
        self._sort_order = choice
        self.load_shipments()

    def build_table(self, rows):
        for widget in self.table.winfo_children():
            widget.destroy()

        if not rows:
            ctk.CTkLabel(self.table, text="No shipments logged.").pack(pady=20)
            return

        headers = ["Shipment ID", "Supplier Name", "Shipment Date", "Reference No.", "Status", "", ""]
        widths   = [100,           200,              150,             150,             120,      120, 110]

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x", pady=2)
        for h, w in zip(headers, widths):
            ctk.CTkLabel(header, text=h, width=w, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            shipment_id = row.get("shipment_id")
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            values = [
                row.get("shipment_id"),
                row.get("supplier_name"),
                row.get("shipment_date"),
                row.get("reference_number"),
                row.get("status"),
            ]

            for v, w in zip(values, widths):
                ctk.CTkLabel(line, text=str(v), width=w, anchor="w").pack(side="left", padx=5)

            ctk.CTkButton(
                line, text="View Items", width=100,
                command=lambda sid=shipment_id: self.open_items_window(sid)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                line, text="Update Status", width=110,
                command=lambda sid=shipment_id, cur=row.get("status"): self.open_status_window(sid, cur)
            ).pack(side="left", padx=4)

    def load_shipments(self):
        try:
            rows = db.get_shipments()
            reverse = self._sort_order == "DESC"
            rows = sorted(rows, key=self._sort_key, reverse=reverse)
            self.build_table(rows)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search(self):
        term = self.search_entry.get().strip().lower()
        if not term:
            self.load_shipments()
            return

        try:
            rows = db.get_shipments()
            filtered = [
                r for r in rows
                if term in str(r.get("supplier_name", "")).lower()
                or term in str(r.get("reference_number", "")).lower()
                or term in str(r.get("status", "")).lower()
            ]
            reverse = self._sort_order == "DESC"
            filtered = sorted(filtered, key=self._sort_key, reverse=reverse)
            self.build_table(filtered)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_shipment_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Log Supplier Shipment")
        form.geometry("360x300")
        form.grab_set()

        fields = ["Supplier ID", "Shipment Date (YYYY-MM-DD)", "Reference Number"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(form, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(form, width=280)
            entry.pack()
            entries[field] = entry

        import datetime
        entries["Shipment Date (YYYY-MM-DD)"].insert(0, str(datetime.date.today()))

        def save():
            try:
                sup_id  = int(entries["Supplier ID"].get().strip())
                s_date  = entries["Shipment Date (YYYY-MM-DD)"].get().strip()
                ref_num = entries["Reference Number"].get().strip()

                if not ref_num:
                    raise ValueError("Reference Number cannot be empty.")

                db.create_shipment(sup_id, s_date, ref_num)
                form.destroy()
                self.load_shipments()
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)

    def open_status_window(self, shipment_id, current_status):
        win = ctk.CTkToplevel(self)
        win.title(f"Update Shipment #{shipment_id}")
        win.geometry("300x220")
        win.grab_set()

        ctk.CTkLabel(win, text=f"Shipment #{shipment_id}", font=("Arial", 14, "bold")).pack(pady=(16, 4))
        ctk.CTkLabel(win, text=f"Current status: {current_status}").pack(pady=(0, 12))

        is_delivered = (current_status or "").upper() == "DELIVERED"

        if is_delivered:
            ctk.CTkLabel(
                win,
                text="This shipment is DELIVERED.\nStock has already been updated.",
                text_color="gray",
                justify="center",
            ).pack(pady=(0, 12))
            ctk.CTkButton(win, text="Close", command=win.destroy).pack(pady=8)
            return

        status_combo = ctk.CTkComboBox(win, values=["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"], width=220)
        status_combo.set(current_status or "PENDING")
        status_combo.pack()

        def save():
            new_status = status_combo.get()
            try:
                db.update_shipment_status(shipment_id, new_status)
                win.destroy()
                self.load_shipments()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(win, text="Save Status", command=save).pack(pady=16)

    def open_items_window(self, shipment_id):
        win = ctk.CTkToplevel(self)
        win.title(f"Shipment #{shipment_id} — Items")
        win.geometry("620x420")
        win.grab_set()

        ctk.CTkLabel(win, text=f"Items in Shipment #{shipment_id}", font=("Arial", 16, "bold")).pack(anchor="w", padx=16, pady=(12, 12))
        ctk.CTkButton(win, text="+ Add Item", command=lambda: self.open_add_item_form(shipment_id, win)).pack(anchor="w", padx=16, pady=(0, 8))

        list_frame_container = ctk.CTkFrame(win, fg_color="transparent")
        list_frame_container.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        def refresh_items():
            for w in list_frame_container.winfo_children():
                w.destroy()

            col_frame = ctk.CTkScrollableFrame(list_frame_container, fg_color="white")
            col_frame.pack(fill="both", expand=True)

            headers = ["Item ID", "Product", "Qty", "Unit Cost", "Total Cost"]
            widths   = [70,        200,        60,    100,          100]

            hdr = ctk.CTkFrame(col_frame, fg_color="#e5e7eb")
            hdr.pack(fill="x")
            for h, w in zip(headers, widths):
                ctk.CTkLabel(hdr, text=h, width=w, anchor="w", font=("Arial", 11, "bold")).pack(side="left", padx=4)

            try:
                items = db.get_items_for_shipment(shipment_id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return

            if not items:
                ctk.CTkLabel(col_frame, text="No items logged for this shipment.").pack(pady=10)
                return

            for item in items:
                r = ctk.CTkFrame(col_frame, fg_color="transparent")
                r.pack(fill="x", pady=1)
                row_vals = [
                    item.get("shipment_item_id"),
                    item.get("product_name"),
                    item.get("quantity"),
                    f"{item.get('unit_cost'):,.2f}",
                    f"{item.get('total_cost'):,.2f}",
                ]
                for v, w in zip(row_vals, widths):
                    ctk.CTkLabel(r, text=str(v), width=w, anchor="w").pack(side="left", padx=4)

        win._refresh_items = refresh_items
        refresh_items()

    def open_add_item_form(self, shipment_id, parent_win):
        form = ctk.CTkToplevel(parent_win)
        form.title("Add Item to Shipment")
        form.geometry("380x300")
        form.grab_set()

        try:
            products = db.get_products()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            form.destroy()
            return

        product_map = {f"{p['product_name']} (#{p['product_id']})": p for p in products}
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

        ctk.CTkLabel(form, text="Unit Cost").pack(pady=(10, 0))
        cost_entry = ctk.CTkEntry(form, width=320)
        cost_entry.pack()

        def save():
            try:
                chosen    = product_combo.get()
                p         = product_map.get(chosen)
                if not p:
                    raise ValueError("Please select a valid product.")
                product_id = p["product_id"]
                quantity   = int(qty_entry.get().strip())
                unit_cost  = float(cost_entry.get().strip())
                if quantity <= 0 or unit_cost <= 0:
                    raise ValueError("Quantity and cost must be positive.")
                db.add_shipment_item(shipment_id, product_id, quantity, unit_cost)
                form.destroy()
                parent_win._refresh_items()
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Add Item", command=save).pack(pady=16)