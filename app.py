import customtkinter as ctk
from config.setup import carregar_chave
from cryptography.fernet import Fernet
from views.login import LoginView
from views.menu import MenuView
from views.nova_password import NovaPasswordView
from views.passwords import PasswordsView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Passwords")
        self.geometry("400x500")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Rodapé
        ctk.CTkLabel(self, text="Created by N0B0DY", font=("Arial", 9), text_color="gray").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self, text="v0.1", font=("Arial", 9), text_color="gray").grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.fernet = None
        self.nome_bd = None
        self.view_atual = None

        self.mostrar_login()

    def mostrar_view(self, view):
        if self.view_atual:
            self.view_atual.destroy()
        self.view_atual = view
        self.view_atual.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def mostrar_login(self):
        self.mostrar_view(LoginView(self, self.ao_fazer_login))

    def ao_fazer_login(self, fernet, nome_bd):
        self.fernet = fernet
        self.nome_bd = nome_bd
        self.mostrar_menu()

    def mostrar_menu(self):
        callbacks = {
            "nova_password": self.mostrar_nova_password,
            "passwords": self.mostrar_passwords,
            "sair": self.mostrar_login,
        }
        self.mostrar_view(MenuView(self, callbacks))

    def mostrar_nova_password(self):
        self.mostrar_view(NovaPasswordView(self, self.nome_bd, self.fernet, self.mostrar_menu))

    def mostrar_passwords(self):
        self.mostrar_view(PasswordsView(self, self.nome_bd, self.fernet, self.mostrar_menu))


if __name__ == "__main__":
    app = App()
    app.mainloop()