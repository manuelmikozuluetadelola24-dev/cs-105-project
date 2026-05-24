import customtkinter
import tkinter

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._login_user = tkinter.StringVar(self)
        self._login_pass = tkinter.StringVar(self)
        self.login_user_entry = customtkinter.CTkEntry(self, placeholder_text="Enter username", textvariable=self._login_user)
        self.login_password_entry = customtkinter.CTkEntry(self, placeholder_text="Enter password", textvariable=self._login_pass)
        self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        self.login_user_entry.grid(row=0, column=0)
        self.login_password_entry.grid(row=1, column=0)
        self.login_button.grid(row=2, column=0)
        self.login_button.configure(fg_color="#009bba", text_color="#FFFFFF")

    def login(self):
        login_credentials = []
        login_credentials.append(self.login_user_entry.get())
        login_credentials.append(self.login_password_entry.get())
        print(login_credentials)
        return login_credentials
