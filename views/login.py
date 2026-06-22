import customtkinter as ctk
from config.setup import carregar_chave, verificar_login
from cryptography.fernet import Fernet
from utils.paths import get_caminho
import os


class LoginView(ctk.CTkFrame):
    def __init__(self, parent, ao_fazer_login):
        super().__init__(parent)
        self.parent = parent
        self.ao_fazer_login = ao_fazer_login

        self.grid_columnconfigure(0, weight=1)

        if not os.path.exists(get_caminho("config.txt")):
            self.mostrar_criar_bd()
        else:
            self.mostrar_login()

    def mostrar_criar_bd(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="🔐 Gestor de Passwords", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=30)
        ctk.CTkLabel(self, text="Primeira vez? Cria a tua base de dados!", font=("Arial", 12)).grid(row=1, column=0, padx=20)

        ctk.CTkLabel(self, text="Nome da base de dados:").grid(row=2, column=0, padx=20, pady=(20, 0), sticky="w")
        self.entrada_nome_bd = ctk.CTkEntry(self, placeholder_text="ex: minhas_passwords")
        self.entrada_nome_bd.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Define a tua password:").grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        self.entrada_nova_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entrada_nova_password.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        self.erro_label = ctk.CTkLabel(self, text="", text_color="red")
        self.erro_label.grid(row=6, column=0)

        ctk.CTkButton(self, text="Criar", command=self.criar_bd).grid(row=7, column=0, padx=20, pady=10, sticky="ew")

    def mostrar_login(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="🔐 Gestor de Passwords", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=30)

        self.entrada_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entrada_password.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.erro_label = ctk.CTkLabel(self, text="", text_color="red")
        self.erro_label.grid(row=2, column=0)

        ctk.CTkButton(self, text="Entrar", command=self.fazer_login).grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    def criar_bd(self):
        nome_bd = self.entrada_nome_bd.get().strip()
        password = self.entrada_nova_password.get()

        if not nome_bd:
            self.erro_label.configure(text="Introduz um nome para a base de dados!")
            return
        if not password:
            self.erro_label.configure(text="Define uma password!")
            return

        chave = carregar_chave()
        fernet = Fernet(chave)

        password_encriptada = fernet.encrypt(password.encode()).decode()
        nome_ficheiro = nome_bd + ".xlsx"

        with open(get_caminho("config.txt"), "w") as f:
            f.write(nome_ficheiro + "\n")
            f.write(password_encriptada + "\n")

        import openpyxl
        caminho_xlsx = get_caminho(nome_ficheiro)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Passwords"
        ws.append(["Descrição", "Password"])
        wb.save(caminho_xlsx)

        dados = open(caminho_xlsx, "rb").read()
        open(caminho_xlsx, "wb").write(fernet.encrypt(dados))

        self.ao_fazer_login(fernet, caminho_xlsx)

    def fazer_login(self):
        chave = carregar_chave()
        fernet = Fernet(chave)
        password_input = self.entrada_password.get()

        nome_bd, erro = verificar_login(fernet, password_input)

        if erro:
            self.erro_label.configure(text=erro)
            return

        self.ao_fazer_login(fernet, nome_bd)
