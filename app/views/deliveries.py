import customtkinter as ctk
import db.db as db

class DeliveriesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ctk.CTkLabel(self, text="Deliveries", font=ctk.CTkFont(size=20, weight="bold")).pack(padx=20, anchor="w", pady=(20, 10) )

        # Add button
        ctk.CTkButton(self, text="+ Add Delivery", command=self.open_add_form).pack(padx=20, anchor="w", pady=(0, 10))

        # Sort by Buttons
        self.sort_by_button = ctk.CTkComboBox(self, values=["`delivery_id`", "`order_id`", "`delivery_date`", "`delivery_street`", "`delivery_barangay`", "`delivery_city`", "`delivery_province`", "`delivered_by`", "`status`"], command=self.set_sort_by)
        self.sort_by_button.pack(pady=(0, 10), anchor="w", padx=20)
        self._sort_by = "`DELIVERY`.`delivery_id`"

        self.sort_order_button = ctk.CTkComboBox(self, values=["DESC", "ASC"], command=self.set_sort_order)
        self.sort_order_button.pack(pady=(0, 10), anchor="w", padx=20)
        self._sort_order = "DESC"

        # Table headers
        headers = ctk.CTkFrame(self)
        headers.pack(fill="x", padx=20)
        for col, width in [("Delivery ID", 70), ("Order ID", 16), ("Delivery date", 120), ("Street", 120), ("Baranggay", 120), ("City", 120), ("Province", 120), ("Delivered by", 120), ("Status", 24)]:
            ctk.CTkLabel(headers, text=col, width=width, font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left", padx=5)

        # Scrollable list
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_deliveries()

    def set_sort_by(self, sort_by_button_choice):
        self._sort_by = "`DELIVERY`." + sort_by_button_choice
        self.load_deliveries()

    def set_sort_order(self, sort_in_button_choice):
        self._sort_order = sort_in_button_choice
        self.load_deliveries()

    def load_deliveries(self):
        # Clear existing rows
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        conn = db.initializeConnection()
        rows = db.listDeliveries(conn, order=self._sort_order, order_by=self._sort_by)
        print(rows)

        for row in rows:
            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            for value, width in zip(row, [70, 70, 120, 120, 120, 120, 120, 120, 24]):
                ctk.CTkLabel(row_frame, text=str(value), width=width, anchor="w").pack(side="left", padx=5)

    def open_add_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Add Delivery")
        form.geometry("400x450")
        form.lift()                    
        form.attributes("-topmost", True)

        fields = ["Delivery Date", "Street", "Barangay", "City", "Province", "Delivered By", "Status"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(form, text=field).pack(pady=(10, 0))
            entry = ctk.CTkEntry(form, width=300)
            entry.pack()
            entries[field] = entry

        def save():
            conn = db.initializeConnection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO DELIVERY (order_id, delivery_date, delivery_street, delivery_barangay, delivery_city, delivery_province, delivered_by, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                entries["Order ID"].get(),
                entries["Delivery Date"].get(),
                entries["Street"].get(),
                entries["Barangay"].get(),
                entries["City"].get(),
                entries["Province"].get(),
                entries["Delivered By"].get(),
                entries["Status"].get()
            ))
            conn.commit()
            conn.close()
            form.destroy()
            self.load_deliveries()

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)
