import customtkinter as ctk

class DashboardView(ctk.CTk):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.title("Delola Store - Dashboard")
        self.geometry("900x600")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="Delola Store", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.sidebar, text=f"Role: {self.role}", text_color="gray").pack(pady=(0, 20))

        # Menu buttons — both roles
        ctk.CTkButton(self.sidebar, text="Orders", command=lambda: self.show("Orders")).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="Customers", command=lambda: self.show("Customers")).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="Deliveries", command=lambda: self.show("Deliveries")).pack(pady=5, padx=10)

        # Owner-only buttons
        if self.role == "Owner":
            ctk.CTkButton(self.sidebar, text="Products", command=lambda: self.show("Products")).pack(pady=5, padx=10)
            ctk.CTkButton(self.sidebar, text="Inventory", command=lambda: self.show("Inventory")).pack(pady=5, padx=10)
            ctk.CTkButton(self.sidebar, text="Suppliers", command=lambda: self.show("Suppliers")).pack(pady=5, padx=10)
            ctk.CTkButton(self.sidebar, text="Shipments", command=lambda: self.show("Shipments")).pack(pady=5, padx=10)

        # Main content area
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.content_label = ctk.CTkLabel(self.main_frame, text="Select a menu item", font=ctk.CTkFont(size=18))
        self.content_label.pack(expand=True)

    def show(self, section):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if section == "Customers":
            try:
                from views.customers import CustomersView
                CustomersView(self.main_frame).pack(fill="both", expand=True)
            except Exception as e:
                ctk.CTkLabel(self.main_frame, text=f"Error: {e}", font=ctk.CTkFont(size=14), text_color="red").pack(expand=True)
        else:
            ctk.CTkLabel(self.main_frame, text=f"{section} — coming soon", font=ctk.CTkFont(size=18)).pack(expand=True)
