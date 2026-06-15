import customtkinter as ctk
from database.db import get_passwords, apagar_password


class VerPasswordsView(ctk.CTkFrame):
    def __init__(self, parent, nome_bd, fernet, ao_voltar):
        super().__init__(parent)
        self.nome_bd = nome_bd
        self.fernet = fernet
        self.ao_voltar = ao_voltar

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="👁 Ver Passwords", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=20)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)
        self.scroll.grid_columnconfigure(1, weight=1)
        self.scroll.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(self.scroll, text="Descrição", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.scroll, text="Password", font=("Arial", 13, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkButton(self, text="⬅ Voltar", fg_color="transparent", border_width=2, command=self.ao_voltar).grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.carregar_lista()

    def carregar_lista(self):
        # Limpa a lista antes de recarregar
        for widget in self.scroll.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.scroll, text="Descrição", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.scroll, text="Password", font=("Arial", 13, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        linhas = get_passwords(self.nome_bd, self.fernet)
        for i, linha in enumerate(linhas, start=1):
            ctk.CTkLabel(self.scroll, text=linha[0]).grid(row=i, column=0, padx=10, pady=3, sticky="w")
            ctk.CTkLabel(self.scroll, text=linha[1]).grid(row=i, column=1, padx=10, pady=3, sticky="w")
            ctk.CTkButton(
                self.scroll,
                text="🗑",
                width=30,
                fg_color="transparent",
                text_color="red",
                hover_color="#3a0000",
                command=lambda idx=i: self.confirmar_apagar(idx)
            ).grid(row=i, column=2, padx=5, pady=3)

    def confirmar_apagar(self, indice):
        popup = ctk.CTkToplevel(self)
        popup.title("Tens a certeza?")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.grab_set()
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(popup, text="Tens a certeza que queres apagar?", wraplength=250).grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        ctk.CTkButton(
            popup,
            text="Sim",
            fg_color="red",
            hover_color="#3a0000",
            command=lambda: self.apagar(indice, popup)
        ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(
            popup,
            text="Não",
            fg_color="transparent",
            border_width=2,
            command=popup.destroy
        ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def apagar(self, indice, popup):
        popup.destroy()
        apagar_password(self.nome_bd, self.fernet, indice)
        self.carregar_lista()