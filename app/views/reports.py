import customtkinter as ctk
from tkinter import messagebox
import db.db as db


class ReportsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Reports", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        # Report selector buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10), padx=20)

        self._report_buttons = {}
        report_tabs = [
            ("Inventory Stock",   self._load_inventory_stock),
            ("Supplier Shipments",self._load_supplier_shipments),
            ("Sales/Orders",      self._load_sales_orders),
            ("Order Items Detail",self._load_order_items),
            ("Low Stock Alert",   self._load_low_stock),
            ("Delivery Status",   self._load_delivery_status),
        ]

        for label, cmd in report_tabs:
            btn = ctk.CTkButton(button_frame, text=label, command=lambda c=cmd, l=label: self._switch_report(l, c))
            btn.pack(side="left", padx=4)
            self._report_buttons[label] = btn

        # Sort controls
        sort_frame = ctk.CTkFrame(self, fg_color="transparent")
        sort_frame.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(sort_frame, text="Sort by:").pack(side="left", padx=(0, 4))

        self._sort_by_combo = ctk.CTkComboBox(sort_frame, values=[], width=180, command=self._on_sort_change)
        self._sort_by_combo.pack(side="left", padx=4)

        self._sort_order_combo = ctk.CTkComboBox(sort_frame, values=["DESC", "ASC"], width=90, command=self._on_sort_change)
        self._sort_order_combo.set("DESC")
        self._sort_order_combo.pack(side="left", padx=4)

        # Table
        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # State
        self._current_loader = None
        self._current_report = None

        # Sort column options per report
        self._sort_options = {
            "Inventory Stock":    ["product_id", "product_name", "category_name", "stock_quantity", "price"],
            "Supplier Shipments": ["supplier_name", "shipment_id", "shipment_date", "status"],
            "Sales/Orders":       ["order_id", "customer_name", "order_date", "status", "total_price"],
            "Order Items Detail": ["order_id", "customer_name", "product_name", "quantity"],
            "Low Stock Alert":    ["product_id", "product_name", "category_name", "stock_quantity"],
            "Delivery Status":    ["delivery_id", "customer_name", "delivery_date", "status"],
        }

        # Default sort column per report
        self._default_sort = {
            "Inventory Stock":    "stock_quantity",
            "Supplier Shipments": "shipment_date",
            "Sales/Orders":       "order_date",
            "Order Items Detail": "order_id",
            "Low Stock Alert":    "stock_quantity",
            "Delivery Status":    "delivery_id",
        }

        self._switch_report("Inventory Stock", self._load_inventory_stock)

    # -------------------------------------------------------------------------
    # Internals
    # -------------------------------------------------------------------------

    def _switch_report(self, label: str, loader):
        self._current_report = label
        self._current_loader = loader

        # Update sort options for this report
        options = self._sort_options.get(label, [])
        self._sort_by_combo.configure(values=options)
        default = self._default_sort.get(label, options[0] if options else "")
        self._sort_by_combo.set(default)
        self._sort_order_combo.set("DESC")

        loader()

    def _on_sort_change(self, _=None):
        if self._current_loader:
            self._current_loader()

    def _sort_key(self):
        return self._sort_by_combo.get()

    def _sort_order(self):
        return self._sort_order_combo.get()

    _NUMERIC_COLS = {
        "product_id", "stock_quantity", "price",
        "shipment_id", "order_id", "delivery_id",
        "quantity", "selling_price", "item_total", "total_price",
    }

    def _sorted(self, rows: list, key: str) -> list:
        reverse = self._sort_order() == "DESC"

        if key in self._NUMERIC_COLS:
            def sort_key(r):
                val = r.get(key)
                try:
                    return (0, float(val))
                except (TypeError, ValueError):
                    return (1, 0.0)
        else:
            def sort_key(r):
                val = r.get(key)
                return (val is None, str(val or "").lower())

        return sorted(rows, key=sort_key, reverse=reverse)

    def clear_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()

    def build_table(self, rows, headers, widths, key_fields):
        """key_fields: list of dict keys matching headers order."""
        self.clear_table()

        if not rows:
            ctk.CTkLabel(self.table, text="No data found.").pack(pady=20)
            return

        header_frame = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header_frame.pack(fill="x", pady=2)
        for col, (h, w) in enumerate(zip(headers, widths)):
            ctk.CTkLabel(header_frame, text=h, width=w, anchor="w",
                         font=("Arial", 11, "bold"), wraplength=w - 5).grid(row=0, column=col, padx=5, sticky="w")

        for row in rows:
            row_frame = ctk.CTkFrame(self.table, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            for col, (field, width) in enumerate(zip(key_fields, widths)):
                value = row.get(field)
                text = str(value) if value is not None else ""
                ctk.CTkLabel(row_frame, text=text, width=width, anchor="w",
                             font=("Arial", 10)).grid(row=0, column=col, padx=5, sticky="w")

    # -------------------------------------------------------------------------
    # Report loaders
    # -------------------------------------------------------------------------

    def _load_inventory_stock(self):
        try:
            rows = db.get_inventory_stock_report()
            rows = self._sorted(rows, self._sort_key())
            headers   = ["Product ID", "Product Name",  "Category",     "Stock Qty",     "Price"]
            widths    = [80,            180,             150,            100,             100]
            key_fields = ["product_id", "product_name", "category_name","stock_quantity","price"]
            self.build_table(rows, headers, widths, key_fields)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", str(e))

    def _load_supplier_shipments(self):
        try:
            rows = db.get_supplier_shipment_report()
            rows = self._sorted(rows, self._sort_key())
            headers    = ["Supplier Name", "Shipment ID", "Date",          "Reference #",      "Status"]
            widths     = [180,              100,           130,             130,                100]
            key_fields = ["supplier_name", "shipment_id", "shipment_date", "reference_number", "status"]
            self.build_table(rows, headers, widths, key_fields)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", str(e))

    def _load_sales_orders(self):
        try:
            rows = db.get_sales_report()
            rows = self._sorted(rows, self._sort_key())
            headers    = ["Order ID",  "Customer",      "Date",       "Type",       "Status", "Total Price"]
            widths     = [80,           150,             130,          100,          100,      120]
            key_fields = ["order_id", "customer_name", "order_date", "order_type", "status", "total_price"]
            self.build_table(rows, headers, widths, key_fields)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", str(e))

    def _load_order_items(self):
        try:
            rows = db.get_order_items_detail_report()
            rows = self._sorted(rows, self._sort_key())
            headers    = ["Order ID",  "Customer",      "Product",      "Qty",      "Unit Price",    "Total"]
            widths     = [80,           150,             200,            70,         100,             100]
            key_fields = ["order_id", "customer_name", "product_name", "quantity", "selling_price", "item_total"]
            self.build_table(rows, headers, widths, key_fields)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", str(e))

    def _load_low_stock(self):
        try:
            rows = db.get_low_stock_alert_report(10)
            rows = self._sorted(rows, self._sort_key())

            # Add alert level as a derived field
            for r in rows:
                r["alert_level"] = "High" if (r.get("stock_quantity") or 0) <= 5 else "Low"

            headers    = ["Product ID",  "Product Name",  "Category",     "Stock Qty",     "Alert Level"]
            widths     = [80,             180,             150,            100,             100]
            key_fields = ["product_id", "product_name", "category_name", "stock_quantity", "alert_level"]
            self.build_table(rows, headers, widths, key_fields)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", str(e))

    def _load_delivery_status(self):
        try:
            rows = db.get_delivery_status_report()
            rows = self._sorted(rows, self._sort_key())
            headers    = ["Delivery ID",  "Customer",      "Date",          "Delivered By", "Status"]
            widths     = [90,              150,             130,             130,            100]
            key_fields = ["delivery_id", "customer_name", "delivery_date", "delivered_by", "status"]
            self.build_table(rows, headers, widths, key_fields)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", str(e))