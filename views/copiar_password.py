import customtkinter as ctk
import pyperclip
from database.db import get_passwords


class CopiarPasswordView(ctk.CTkFrame):
    def __init__(self, parent, nome_bd, fernet, ao_voltar):
        super().__init__(parent)
        self.nome_bd = nome_bd
        self.fernet = fernet
        self.ao_voltar = ao_voltar

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="📋 Copiar Password", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=20)

        scroll = ctk.CTkScrollableFrame(self)
        scroll.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(scroll, text="Descrição", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.label_copiado = ctk.CTkLabel(self, text="", text_color="green")
        self.label_copiado.grid(row=2, column=0, pady=5)

        linhas = get_passwords(self.nome_bd, self.fernet)
        for i, linha in enumerate(linhas, start=1):
            ctk.CTkLabel(scroll, text=linha[0]).grid(row=i, column=0, padx=10, pady=3, sticky="w")
            ctk.CTkButton(
                scroll,
                text="📋",
                width=30,
                fg_color="transparent",
                text_color="lightblue",
                command=lambda p=linha[1]: self.copiar(p)
            ).grid(row=i, column=1, padx=5, pady=3)

        ctk.CTkButton(self, text="⬅ Voltar", fg_color="transparent", border_width=2, command=self.ao_voltar).grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    def copiar(self, password):
        pyperclip.copy(password)
        self.label_copiado.configure(text="Password copiada! ✅")