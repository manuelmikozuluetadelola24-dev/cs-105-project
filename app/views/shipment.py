import customtkinter as ctk
from tkinter import messagebox
import db.db as db

class ShipmentView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")

        ctk.CTkLabel(self, text="Shipments", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 15))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(top, text="+ Log Shipment", command=self.add_shipment_form).pack(side="left", padx=4)
        ctk.CTkButton(top, text="Refresh", command=self.load_shipments).pack(side="left", padx=4)

        self.table = ctk.CTkScrollableFrame(self, fg_color="white")
        self.table.pack(fill="both", expand=True)

        self.load_shipments()

    def load_shipments(self):
        for widget in self.table.winfo_children():
            widget.destroy()

        try:
            rows = db.get_shipments()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not rows:
            ctk.CTkLabel(self.table, text="No shipments logged.").pack(pady=20)
            return

        headers = ["Shipment ID", "Supplier Name", "Shipment Date", "Reference No.", "Status"]
        widths = [100, 200, 150, 150, 120]

        header = ctk.CTkFrame(self.table, fg_color="#e5e7eb")
        header.pack(fill="x", pady=2)

        for h, w in zip(headers, widths):
            ctk.CTkLabel(header, text=h, width=w, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for row in rows:
            line = ctk.CTkFrame(self.table, fg_color="transparent")
            line.pack(fill="x", pady=2)

            values = [
                row.get("shipment_id"),
                row.get("supplier_name"),
                row.get("shipment_date"),
                row.get("reference_number"),
                row.get("status")
            ]

            for v, w in zip(values, widths):
                ctk.CTkLabel(line, text=str(v), width=w, anchor="w").pack(side="left", padx=5)

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
                sup_id = int(entries["Supplier ID"].get().strip())
                s_date = entries["Shipment Date (YYYY-MM-DD)"].get().strip()
                ref_num = entries["Reference Number"].get().strip()

                if not ref_num:
                    raise ValueError("Reference Number cannot be empty.")

                db.create_shipment(sup_id, s_date, ref_num)
                form.destroy()
                self.load_shipments()
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

        ctk.CTkButton(form, text="Save", command=save).pack(pady=20)