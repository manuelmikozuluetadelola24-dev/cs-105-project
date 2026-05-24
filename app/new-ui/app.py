import customtkinter
import login


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x480")
        self.title("delola store database client")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.changeScreen(self.loginScreen)
    
    def changeScreen(self, newScreen):
        newScreen()
    
    def loginScreen(self):
        self.loginScreen = login.LoginFrame(self)
        self.loginScreen.grid(row=0, column=0)
        
app = App()
app.mainloop()
