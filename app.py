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
        self.geometry("500x600")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(600, 400)

        # Rodapé
        ctk.CTkLabel(self, text="Created by Tiaguin", font=("Arial", 9), text_color="gray").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        from utils.updater import get_versao_atual
        ctk.CTkLabel(self, text=f"v{get_versao_atual()}", font=("Arial", 9), text_color="gray").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        
        self.fernet = None
        self.nome_bd = None
        self.view_atual = None

        self.mostrar_login()

        # Verifica atualizações após a app abrir
        self.after(1000, self.verificar_atualizacao)

    def verificar_atualizacao(self):
        from utils.updater import verificar_atualizacao, URL_DOWNLOAD
        import webbrowser

        versao_nova = verificar_atualizacao()
        if not versao_nova:
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Atualização disponível")
        popup.geometry("300x180")
        popup.resizable(False, False)
        popup.grab_set()
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(popup, text=f"🆕 Nova versão disponível: {versao_nova}", font=("Arial", 13, "bold"), wraplength=260).grid(row=0, column=0, columnspan=2, pady=20, padx=20)
        ctk.CTkLabel(popup, text="Queres atualizar agora?", wraplength=260).grid(row=1, column=0, columnspan=2, padx=20)

        ctk.CTkButton(
            popup,
            text="Atualizar",
            command=lambda: [webbrowser.open(URL_DOWNLOAD), popup.destroy()]
        ).grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        ctk.CTkButton(
            popup,
            text="Agora não",
            fg_color="transparent",
            border_width=2,
            command=popup.destroy
        ).grid(row=2, column=1, padx=10, pady=15, sticky="ew")

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