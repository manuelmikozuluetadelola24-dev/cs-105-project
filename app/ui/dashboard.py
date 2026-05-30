import customtkinter as ctk

try:
    import db.db as db
except ImportError:
    from app.db import db


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#f4f6f9")
        self.pack(fill="both", expand=True)

        counts = db.get_dashboard_counts()

        welcome = ctk.CTkLabel(
            self,
            text="Welcome to Delola Store Product Management System",
            font=("Arial", 20, "bold"),
            text_color="#111827",
        )
        welcome.pack(anchor="w", pady=(0, 20))

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x")

        self.card(cards_frame, "Total Products", counts.get("total_products", 0), "Items in inventory").grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.card(cards_frame, "Low Stock", counts.get("low_stock", 0), "Products need restock").grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.card(cards_frame, "Pending Orders", counts.get("pending_orders", 0), "Orders to process").grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.card(cards_frame, "Pending Deliveries", counts.get("pending_deliveries", 0), "Deliveries in progress").grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        info_box = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        info_box.pack(fill="both", expand=True, pady=25)

        ctk.CTkLabel(
            info_box,
            text="System Overview",
            font=("Arial", 18, "bold"),
            text_color="#111827",
        ).pack(anchor="w", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            info_box,
            text="Use the sidebar to manage products, customers, orders, shipments, deliveries, and reports.",
            font=("Arial", 14),
            text_color="#64748b",
        ).pack(anchor="w", padx=20, pady=5)

    def card(self, parent, title, value, subtitle):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 14, "bold"),
            text_color="#64748b",
        ).pack(anchor="w", padx=18, pady=(18, 5))

        ctk.CTkLabel(
            frame,
            text=str(value),
            font=("Arial", 30, "bold"),
            text_color="#2563eb",
        ).pack(anchor="w", padx=18)

        ctk.CTkLabel(
            frame,
            text=subtitle,
            font=("Arial", 12),
            text_color="#94a3b8",
        ).pack(anchor="w", padx=18, pady=(5, 18))

        return frame