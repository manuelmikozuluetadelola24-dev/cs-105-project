"""Login frame for Delola Store."""

import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import db.db as db


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_login_success=None):
        super().__init__(master, fg_color="white", corner_radius=18)

        self.on_login_success = on_login_success

        ctk.CTkLabel(
            self,
            text="Delola Store",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).grid(row=0, column=0, padx=40, pady=(35, 20))

        self.username_entry = ctk.CTkEntry(
            self,
            width=280,
            placeholder_text="Username",
        )
        self.username_entry.grid(row=1, column=0, padx=40, pady=8)

        self.password_entry = ctk.CTkEntry(
            self,
            width=280,
            placeholder_text="Password",
            show="*",
        )
        self.password_entry.grid(row=2, column=0, padx=40, pady=8)

        self.login_button = ctk.CTkButton(
            self,
            width=280,
            text="Login",
            command=self.login,
        )
        self.login_button.grid(row=3, column=0, padx=40, pady=(16, 35))

        self.password_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Error", "Enter username and password.")
            return

        try:
            user = db.get_user_by_credentials(username, password)

            if not user:
                messagebox.showerror("Login Error", "Invalid username or password.")
                return

            if self.on_login_success:
                self.on_login_success(user)
            elif hasattr(self.master, "show_dashboard"):
                self.master.show_dashboard(user)
            elif hasattr(self.master, "changeScreen") and hasattr(self.master, "dashboardScreen"):
                self.master.changeScreen(self.master.dashboardScreen)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))