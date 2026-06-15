import customtkinter as ctk
from database.db import get_passwords, editar_password


class EditarPasswordView(ctk.CTkFrame):
    def __init__(self, parent, nome_bd, fernet, ao_voltar, ao_recarregar):
        super().__init__(parent)
        self.nome_bd = nome_bd
        self.fernet = fernet
        self.ao_voltar = ao_voltar
        self.ao_recarregar = ao_recarregar  # callback para recarregar a view

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="✏️ Editar Password", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=20)

        scroll = ctk.CTkScrollableFrame(self)
        scroll.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)
        scroll.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(scroll, text="Descrição", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(scroll, text="Password", font=("Arial", 13, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        linhas = get_passwords(self.nome_bd, self.fernet)
        for i, linha in enumerate(linhas, start=1):
            ctk.CTkLabel(scroll, text=linha[0]).grid(row=i, column=0, padx=10, pady=3, sticky="w")
            ctk.CTkLabel(scroll, text=linha[1]).grid(row=i, column=1, padx=10, pady=3, sticky="w")
            ctk.CTkButton(
                scroll,
                text="✏️",
                width=30,
                fg_color="transparent",
                text_color="lightblue",
                command=lambda idx=i, d=linha[0], p=linha[1]: self.popup_editar(idx, d, p)
            ).grid(row=i, column=2, padx=5, pady=3)

        ctk.CTkButton(self, text="⬅ Voltar", fg_color="transparent", border_width=2, command=self.ao_voltar).grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def popup_editar(self, indice, descricao, password):
        popup = ctk.CTkToplevel(self)
        popup.title("Editar Password")
        popup.geometry("350x300")
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
        self.ao_recarregar()  # recarrega a view após editar