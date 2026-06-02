import customtkinter as ctk
import login


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Delola Store")
        self.geometry("1200x720")
        ctk.set_appearance_mode("light")
        self.content = None
        self.user = None
        self.show_login()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()
        login.LoginFrame(self, on_login_success=self.show_dashboard).pack(expand=True)

    def show_dashboard(self, user=None):
        self.user = user
        self.clear_screen()

        sidebar = ctk.CTkFrame(self, width=220, fg_color="#111827", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="Delola Store", font=("Arial", 22, "bold"), text_color="white").pack(
            anchor="w", padx=20, pady=(30, 10)
        )

        role = (user.get("role") or "EMPLOYEE") if user else "OWNER"
        ctk.CTkLabel(sidebar, text=f"Role: {role}", text_color="#cbd5e1").pack(anchor="w", padx=20, pady=(0, 20))

        self.content = ctk.CTkFrame(self, fg_color="#f4f6f9")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        pages = [
            ("Dashboard", self.open_dashboard),
            ("Products", self.open_products),
            ("Customers", self.open_customers),
            ("Orders", self.open_orders),
            ("Suppliers", self.open_suppliers),
            ("Shipments", self.open_shipments),
            ("Deliveries", self.open_deliveries),
            ("Reports", self.open_reports),
            ("Logout", self.show_login),
        ]

        for text, command in pages:
            if role == "EMPLOYEE" and text in ["Products", "Suppliers", "Shipments", "Reports"]:
                continue

            ctk.CTkButton(
                sidebar,
                text=text,
                anchor="w",
                fg_color="transparent",
                hover_color="#1f2937",
                command=command,
            ).pack(fill="x", padx=12, pady=5)

        self.open_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def open_dashboard(self):
        self.clear_content()
        from ui.dashboard import DashboardPage
        DashboardPage(self.content)

    def open_products(self):
        self.clear_content()
        from views.products import ProductsView
        ProductsView(self.content).pack(fill="both", expand=True)

    def open_customers(self):
        self.clear_content()
        from views.customers import CustomersView
        CustomersView(self.content).pack(fill="both", expand=True)

    def open_orders(self):
        self.clear_content()
        from views.orders import OrdersView
        OrdersView(self.content).pack(fill="both", expand=True)

    def open_suppliers(self):
        self.clear_content()
        from views.suppliers import SuppliersView
        SuppliersView(self.content).pack(fill="both", expand=True)

    def open_shipments(self):
        self.clear_content()
        from views.shipment import ShipmentView
        ShipmentView(self.content).pack(fill="both", expand=True)

    def open_deliveries(self):
        self.clear_content()
        from views.deliveries import DeliveriesView
        DeliveriesView(self.content).pack(fill="both", expand=True)

    def open_reports(self):
        self.clear_content()
        from views.reports import ReportsView
        ReportsView(self.content).pack(fill="both", expand=True)


if __name__ == "__main__":
    App().mainloop()