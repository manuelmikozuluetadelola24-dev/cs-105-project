import customtkinter as ctk
import db.db as db

class CustomersView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ctk.CTkLabel(self, text="Customers", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10), anchor="w", padx=20)

        # Add button
        ctk.CTkButton(self, text="+ Add Customer", command=self.open_add_form).pack(pady=(0, 10), anchor="w", padx=20)

        # Table headers
        headers = ctk.CTkFrame(self)
        headers.pack(fill="x", padx=20)
        for col, width in [("ID", 50), ("Name", 200), ("Contact", 120), ("City", 120), ("Province", 120)]:
            ctk.CTkLabel(headers, text=col, width=width, font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left", padx=5)

        # Scrollable list
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_customers()

    def load_customers(self):
        # Clear existing rows
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        conn = db.initializeConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, customer_name, contact_number, customer_city, customer_province FROM CUSTOMER")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            for value, width in zip(row, [50, 200, 120, 120, 120]):
                ctk.CTkLabel(row_frame, text=str(value), width=width, anchor="w").pack(side="left", padx=5)

    def open_add_form(self):
        form = ctk.CTkToplevel(self)
        form.title("Add Customer")
        form.geometry("400x450")
        form.lift()                    
        form.attributes("-topmost", True)

        fields = ["Name", "Contact Number", "Street", "Barangay", "City", "Province"]
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
                INSERT INTO CUSTOMER (customer_name, contact_number, customer_street, customer_barangay, customer_city, customer_province)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                entries["Name"].get(),
                entries["Contact Number"].get(),
                entries["Street"].get(),
                entries["Barangay"].get(),
                entries["City"].get(),
                entries["Province"].get()
            ))
            conn.commit()
            conn.close()
            form.destroy()
            self.load_customers()

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)
