import customtkinter as ctk
import random
import string
from database.db import adicionar_password, get_passwords


class NovaPasswordView(ctk.CTkFrame):
    def __init__(self, parent, nome_bd, fernet, ao_voltar):
        super().__init__(parent)
        self.nome_bd = nome_bd
        self.fernet = fernet
        self.ao_voltar = ao_voltar
        self.password_gerada = ""

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="➕ Nova Password", font=("Arial", 22, "bold")).grid(row=0, column=0, columnspan=3, pady=20)

        ctk.CTkLabel(self, text="Descrição:").grid(row=1, column=0, columnspan=3, padx=20, sticky="w")
        self.entrada_descricao = ctk.CTkEntry(self, placeholder_text="ex: email, netflix...")
        self.entrada_descricao.grid(row=2, column=0, columnspan=3, padx=20, pady=5, sticky="ew")
        self.entrada_descricao.bind("<KeyRelease>", self.limitar_descricao)

        # Presets de tamanho
        ctk.CTkLabel(self, text="Tamanho:").grid(row=3, column=0, columnspan=3, padx=20, sticky="w")

        self.tamanho = ctk.IntVar(value=16)

        frame_presets = ctk.CTkFrame(self, fg_color="transparent")
        frame_presets.grid(row=4, column=0, columnspan=3, padx=20, pady=5, sticky="ew")
        frame_presets.grid_columnconfigure(0, weight=1)
        frame_presets.grid_columnconfigure(1, weight=1)
        frame_presets.grid_columnconfigure(2, weight=1)

        for i, tamanho in enumerate([16, 32, 64]):
            ctk.CTkRadioButton(
                frame_presets,
                text=f"{tamanho} caracteres",
                variable=self.tamanho,
                value=tamanho
            ).grid(row=0, column=i, padx=5, sticky="w")

        # Checkboxes
        self.usar_letras = ctk.BooleanVar(value=True)
        self.usar_numeros = ctk.BooleanVar(value=True)
        self.usar_simbolos = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(self, text="Letras", variable=self.usar_letras).grid(row=5, column=0, columnspan=3, padx=20, pady=5, sticky="w")
        ctk.CTkCheckBox(self, text="Números", variable=self.usar_numeros).grid(row=6, column=0, columnspan=3, padx=20, pady=5, sticky="w")
        ctk.CTkCheckBox(self, text="Símbolos", variable=self.usar_simbolos).grid(row=7, column=0, columnspan=3, padx=20, pady=5, sticky="w")

        self.label_password_gerada = ctk.CTkLabel(self, text="", font=("Arial", 11), wraplength=320)
        self.label_password_gerada.grid(row=8, column=0, columnspan=3, pady=10)

        ctk.CTkButton(self, text="Gerar Password", command=self.gerar).grid(row=9, column=0, columnspan=3, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self, text="Guardar", command=self.guardar).grid(row=10, column=0, columnspan=3, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self, text="⬅ Voltar", fg_color="transparent", border_width=2, command=self.ao_voltar).grid(row=11, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

    def gerar(self):
        caracteres = ""
        if self.usar_letras.get():
            caracteres += string.ascii_letters
        if self.usar_numeros.get():
            caracteres += string.digits
        if self.usar_simbolos.get():
            caracteres += string.punctuation

        if not caracteres:
            self.label_password_gerada.configure(text="Escolhe pelo menos um tipo!", text_color="red")
            return

        tamanho = self.tamanho.get()
        self.password_gerada = "".join(random.choice(caracteres) for _ in range(tamanho))
        self.label_password_gerada.configure(text=self.password_gerada, text_color="green")

    def limitar_descricao(self, event):
        texto = self.entrada_descricao.get()
        if len(texto) > 32:
            self.entrada_descricao.delete(32, "end")
            
    def guardar(self):
        if not self.password_gerada:
            self.label_password_gerada.configure(text="Gera uma password primeiro!", text_color="red")
            return

        descricao = self.entrada_descricao.get()
        if not descricao:
            self.label_password_gerada.configure(text="Adiciona uma descrição!", text_color="red")
            return

        linhas = get_passwords(self.nome_bd, self.fernet)
        descricoes = [linha[0] for linha in linhas]

        if descricao in descricoes:
            self.label_password_gerada.configure(text="Já existe uma password com essa descrição!", text_color="red")
            return

        adicionar_password(self.nome_bd, self.fernet, descricao, self.password_gerada)
        self.password_gerada = ""
        self.label_password_gerada.configure(text="Guardado com sucesso! ✅", text_color="green")