from views.login import LoginView
from views.dashboard import DashboardView

def main():
    login = LoginView()
    login.mainloop()

    if login.logged_in_role:
        dashboard = DashboardView(login.logged_in_role)
        dashboard.mainloop()

main()