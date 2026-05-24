import customtkinter as ctk
import db.db as db

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.logged_in = False
        self.title("Delola Store")
        self.geometry("400x300")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")

        # Title
        ctk.CTkLabel(self, text="Delola Store", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(40, 20))

        self.user_entry = ctk.CTkEntry(self, placeholder_text="User", width=200)
        self.user_entry.pack(pady=(0, 15))
        # Password field
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=200)
        self.password_entry.pack(pady=(0, 15))


        # Login button
        ctk.CTkButton(self, text="Login", width=200, command=self.login).pack()

        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=(10, 0))

    def login(self):
        user = self.user_entry.get()
        password = self.password_entry.get()

        if(db.checkUser(user, password)):
            db.config[1] = user
            db.config[2] = password
            self.logged_in = True
            self.destroy()
        else:
            self.logged_in = False
            print("Error, user does not exist")

