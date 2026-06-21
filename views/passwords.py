import customtkinter as ctk
from database.db import get_passwords, apagar_password, editar_password
import pyperclip


class PasswordsView(ctk.CTkFrame):
    def __init__(self, parent, nome_bd, fernet, ao_voltar):
        super().__init__(parent)
        self.nome_bd = nome_bd
        self.fernet = fernet
        self.ao_voltar = ao_voltar

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="🔐 Passwords", font=("Arial", 22, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=0)  # descrição - fixo
        self.scroll.grid_columnconfigure(1, weight=1)  # password - estica e corta
        self.scroll.grid_columnconfigure(2, weight=0)  # botões - fixo à direita

        ctk.CTkButton(self, text="⬅ Voltar", fg_color="transparent", border_width=2, text_color=("black", "white"), command=self.ao_voltar).grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.carregar_lista()

    def carregar_lista(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        # Cabeçalho
        ctk.CTkLabel(self.scroll, text="Descrição", font=("Arial", 13, "bold"), width=220, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.scroll, text="Password", font=("Arial", 13, "bold"), anchor="w").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        linhas = get_passwords(self.nome_bd, self.fernet)
        for i, linha in enumerate(linhas, start=1):
            ctk.CTkLabel(self.scroll, text=linha[0], width=220, anchor="w", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=3, sticky="w")
            ctk.CTkLabel(self.scroll, text=linha[1], anchor="w", font=("Courier", 12)).grid(row=i, column=1, padx=10, pady=3, sticky="ew")

            # Frame com os 3 botões sempre à direita
            frame_botoes = ctk.CTkFrame(self.scroll, fg_color="transparent")
            frame_botoes.grid(row=i, column=2, padx=5, pady=3, sticky="e")

            ctk.CTkButton(
                frame_botoes,
                text="📋",
                width=30,
                fg_color="transparent",
                text_color="lightblue",
                command=lambda p=linha[1]: self.copiar(p)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                frame_botoes,
                text="✏️",
                width=30,
                fg_color="transparent",
                text_color="lightblue",
                command=lambda idx=i, d=linha[0], p=linha[1]: self.popup_editar(idx, d, p)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                frame_botoes,
                text="🗑",
                width=30,
                fg_color="transparent",
                text_color="red",
                hover_color="#3a0000",
                command=lambda idx=i: self.confirmar_apagar(idx)
            ).pack(side="left", padx=2)

    def copiar(self, password):
        pyperclip.copy(password)

    def confirmar_apagar(self, indice):
        popup = ctk.CTkToplevel(self)
        popup.title("Tens a certeza?")
        popup.geometry("400x150")
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

    def popup_editar(self, indice, descricao, password):
        popup = ctk.CTkToplevel(self)
        popup.title("Editar Password")
        popup.geometry("350x280")
        popup.resizable(False, False)
        popup.grab_set()
        popup.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(popup, text="Editar Password", font=("Arial", 18, "bold")).grid(row=0, column=0, pady=20)

        ctk.CTkLabel(popup, text="Descrição:").grid(row=1, column=0, padx=20, sticky="w")
        entrada_descricao = ctk.CTkEntry(popup)
        entrada_descricao.insert(0, descricao)
        entrada_descricao.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(popup, text="Password:").grid(row=3, column=0, padx=20, sticky="w")
        entrada_password = ctk.CTkEntry(popup)
        entrada_password.insert(0, password)
        entrada_password.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkButton(
            popup,
            text="Guardar",
            command=lambda: self.guardar_edicao(indice, entrada_descricao.get(), entrada_password.get(), popup)
        ).grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkButton(
            popup,
            text="Cancelar",
            fg_color="transparent",
            border_width=2,
            command=popup.destroy
        ).grid(row=6, column=0, padx=20, pady=5, sticky="ew")

    def guardar_edicao(self, indice, nova_descricao, nova_password, popup):
        popup.destroy()
        editar_password(self.nome_bd, self.fernet, indice, nova_descricao, nova_password)
        self.carregar_lista()
