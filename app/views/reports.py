from wsgiref import headers

import customtkinter as ctk
from tkinter import messagebox
import db.db as db


class ReportsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Reports", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        # Button frame for report selection
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10), padx=20)

        ctk.CTkButton(button_frame, text="Inventory Stock", command=self.show_inventory_stock).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="Supplier Shipments", command=self.show_supplier_shipments).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="Sales/Orders", command=self.show_sales_orders).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="Order Items Detail", command=self.show_order_items).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="Low Stock Alert", command=self.show_low_stock).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="Delivery Status", command=self.show_delivery_status).pack(side="left", padx=4)

        # Table frame
        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.current_headers = []
        self.show_inventory_stock()

    def clear_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()
        self.current_headers = []

    def build_table(self, rows, headers, widths):
        self.clear_table()

        if not rows:
            ctk.CTkLabel(self.table, text="No data found.").pack(pady=20)
            return

        # Build header
        header_frame = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header_frame.pack(fill="x", pady=2)

        for col, (h, w) in enumerate(zip(headers, widths)):
            lbl = ctk.CTkLabel(header_frame, text=h, width=w, anchor="w",
                               font=("Arial", 11, "bold"), wraplength=w - 5)
            lbl.grid(row=0, column=col, padx=5, sticky="w")

    # Data rows
        for row in rows:
            row_frame = ctk.CTkFrame(self.table, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            for col, (value, width) in enumerate(zip(row, widths)):
                text = str(value) if value is not None else ""
                lbl = ctk.CTkLabel(row_frame, text=text, width=width, anchor="w",
                               font=("Arial", 10))
                lbl.grid(row=0, column=col, padx=5, sticky="w")

    def show_inventory_stock(self):
        try:
            report_data = db.get_inventory_stock_report()
            
            rows = []
            for item in report_data:
                rows.append((
                    item.get("product_id"),
                    item.get("product_name"),
                    item.get("category_name"),
                    item.get("stock_quantity"),
                    f"${item.get('price', 0):.2f}"
                ))

            headers = ["Product ID", "Product Name", "Category", "Stock Qty", "Price"]
            widths = [80, 180, 150, 100, 100]

            self.build_table(rows, headers, widths)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", f"Failed to load inventory stock report: {str(e)}")

    def show_supplier_shipments(self):
        try:
            report_data = db.get_supplier_shipment_report()
            
            rows = []
            for item in report_data:
                rows.append((
                    item.get("supplier_name"),
                    item.get("shipment_id"),
                    item.get("shipment_date"),
                    item.get("reference_number"),
                    item.get("status")
                ))

            headers = ["Supplier Name", "Shipment ID", "Date", "Reference #", "Status"]
            widths = [180, 100, 130, 130, 100]

            self.build_table(rows, headers, widths)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", f"Failed to load supplier shipment report: {str(e)}")

    def show_sales_orders(self):
        try:
            report_data = db.get_sales_report()
            
            rows = []
            for item in report_data:
                rows.append((
                    item.get("order_id"),
                    item.get("customer_name"),
                    item.get("order_date"),
                    item.get("order_type"),
                    item.get("status"),
                    f"${item.get('total_price', 0):.2f}"
                ))

            headers = ["Order ID", "Customer", "Date", "Type", "Status", "Total Price"]
            widths = [80, 150, 130, 100, 100, 120]

            self.build_table(rows, headers, widths)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", f"Failed to load sales/orders report: {str(e)}")

    def show_order_items(self):
        try:
            report_data = db.get_order_items_detail_report()
            
            rows = []
            for item in report_data:
                rows.append((
                    item.get("order_id"),
                    item.get("customer_name"),
                    item.get("product_name"),
                    item.get("quantity"),
                    f"${item.get('selling_price', 0):.2f}",
                    f"${item.get('item_total', 0):.2f}"
                ))

            headers = ["Order ID", "Customer", "Product", "Qty", "Unit Price", "Total"]
            widths = [80, 150, 200, 70, 100, 100]

            self.build_table(rows, headers, widths)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", f"Failed to load order items detail report: {str(e)}")

    def show_low_stock(self):
        try:
            report_data = db.get_low_stock_alert_report(10)
            
            rows = []
            for item in report_data:
                rows.append((
                    item.get("product_id"),
                    item.get("product_name"),
                    item.get("category_name"),
                    item.get("stock_quantity"),
                    "High" if item.get("stock_quantity", 0) <= 5 else "Low"
                ))

            headers = ["Product ID", "Product Name", "Category", "Stock Qty", "Alert Level"]
            widths = [80, 180, 150, 100, 100]

            self.build_table(rows, headers, widths)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", f"Failed to load low stock alert report: {str(e)}")

    def show_delivery_status(self):
        try:
            report_data = db.get_delivery_status_report()
            
            rows = []
            for item in report_data:
                rows.append((
                    item.get("delivery_id"),
                    item.get("customer_name"),
                    item.get("delivery_date"),
                    item.get("delivered_by"),
                    item.get("status")
                ))

            headers = ["Delivery ID", "Customer", "Date", "Delivered By", "Status"]
            widths = [90, 150, 130, 130, 100]

            self.build_table(rows, headers, widths)
        except Exception as e:
            self.clear_table()
            messagebox.showerror("Error", f"Failed to load delivery status report: {str(e)}")
