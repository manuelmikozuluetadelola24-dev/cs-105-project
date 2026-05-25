import customtkinter as ctk
import login


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Delola Store")
        self.geometry("1200x720")
        self.resizable(True, True)

        ctk.set_appearance_mode("light")
        self.current_screen = None
        self.content = None

        self.show_login()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()
        frame = login.LoginFrame(self, on_login_success=self.show_dashboard)
        frame.pack(expand=True)

    def show_dashboard(self, user=None):
        self.clear_screen()

        sidebar = ctk.CTkFrame(self, width=220, fg_color="#111827", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="Delola Store",
            font=("Arial", 22, "bold"),
            text_color="white",
        ).pack(anchor="w", padx=20, pady=(30, 20))

        self.content = ctk.CTkFrame(self, fg_color="#f4f6f9")
        self.content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        buttons = [
            ("Dashboard", self.open_dashboard),
            ("Customers", self.open_customers),
            ("Deliveries", self.open_deliveries),
            ("Orders", self.open_orders),
            ("Shipments", self.open_shipments),
            ("Logout", self.show_login),
        ]

        for text, command in buttons:
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

    def open_customers(self):
        self.clear_content()
        from views.customers import CustomersView
        CustomersView(self.content).pack(fill="both", expand=True)

    def open_deliveries(self):
        self.clear_content()
        from views.deliveries import DeliveriesView
        DeliveriesView(self.content).pack(fill="both", expand=True)

    def open_orders(self):
        self.clear_content()
        from views.orders import OrdersView
        OrdersView(self.content).pack(fill="both", expand=True)

    def open_shipments(self):
        self.clear_content()
        from views.shipment import ShipmentView
        ShipmentView(self.content).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()