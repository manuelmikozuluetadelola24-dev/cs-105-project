import customtkinter as ctk
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
class CustomersView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ctk.CTkLabel(self, text="Customers", font=ctk.CTkFont(size=20, weight="bold")).pack(padx=20, anchor="w", pady=(20, 10) )

        # Add button
        ctk.CTkButton(self, text="+ Add Customer", command=self.open_add_form).pack(padx=20, anchor="w", pady=(0, 10))

        # Sort by Buttons
        self.sort_by_button = ctk.CTkComboBox(self, values=["`customer_id`", "`customer_name`", "`contact_number`", "`customer_street`", "`customer_barangay`", "`customer_city`", "`customer_province`"], command=self.set_sort_by)
        self.sort_by_button.pack(pady=(0, 10), anchor="w", padx=20)
        self._sort_by = "`customer_id`"

        self.sort_order_button = ctk.CTkComboBox(self, values=["DESC", "ASC"], command=self.set_sort_order)
        self.sort_order_button.pack(pady=(0, 10), anchor="w", padx=20)
        self._sort_order = "DESC"

        # Table headers
        headers = ctk.CTkFrame(self)
        headers.pack(fill="x", padx=20)
        for col, width in [("ID", 16), ("Name", 200), ("Contact", 120), ("Street", 120), ("Baranggay", 120), ("City", 120), ("Province", 120)]:
            ctk.CTkLabel(headers, text=col, width=width, font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left", padx=5)

        # Scrollable list
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_customers()

    def set_sort_by(self, sort_by_button_choice):
        self._sort_by = sort_by_button_choice
        self.load_customers()

    def set_sort_order(self, sort_in_button_choice):
        self._sort_order = sort_in_button_choice
        self.load_customers()

    def load_customers(self):
        # Clear existing rows
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        conn = db.initializeConnection()
        rows = db.listCustomers(conn, order=self._sort_order, order_by=self._sort_by)
        print(rows)

        for row in rows:
            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            
            max_chars = [6, 22, 13, 16, 16, 14, 14]

            for value, width, m in zip(row, [16, 200, 120, 120, 120, 120, 120], max_chars):
                text = str(value)
                truncated = f"{text[:m - 1]}…" if len(text) > m else text
                label = ctk.CTkLabel(row_frame, text=truncated, width=width, anchor="w")
                label.pack(side="left", padx=5)
                if len(text) > m:
                    Tooltip(label, text)

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
