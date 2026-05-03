import customtkinter as ctk

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Delola Store")
        self.geometry("400x300")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")

        # Title
        ctk.CTkLabel(self, text="Delola Store", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(40, 20))

        # Role selection
        self.role_var = ctk.StringVar(value="Owner")
        ctk.CTkSegmentedButton(self, values=["Owner", "Employee"], variable=self.role_var).pack(pady=(0, 15))

        # Password field
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=200)
        self.password_entry.pack(pady=(0, 15))

        # Login button
        ctk.CTkButton(self, text="Login", width=200, command=self.login).pack()

        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=(10, 0))

    def login(self):
        role = self.role_var.get()
        password = self.password_entry.get()

        if role == "Owner" and password == "owner123":
            self.destroy()  # closes the login window
            print("Logged in as Owner")
        elif role == "Employee" and password == "emp123":
            self.destroy()  # closes the login window
            print("Logged in as Employee")
        else:
            self.error_label.configure(text="Incorrect password.")