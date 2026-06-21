import customtkinter as ctk
from utils.icons import carregar_icone


class MenuView(ctk.CTkFrame):
    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="🔐 Gestor de Passwords", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=20)

        botoes = [
            ("Nova Password", "plus.png", callbacks["nova_password"]),
            ("Passwords", "list.png", callbacks["passwords"]),
            ("Sair", "logout.png", callbacks["sair"]),
        ]

        for i, (texto, icone, comando) in enumerate(botoes, start=1):
            ctk.CTkButton(
                self,
                text=texto,
                image=carregar_icone(icone),
                anchor="w",
                command=comando
            ).grid(row=i, column=0, padx=20, pady=5, sticky="ew")