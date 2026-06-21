import customtkinter as ctk
import random
import string
from database.db import adicionar_password, get_passwords
from utils.icons import carregar_icone


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

        frame_password = ctk.CTkFrame(self, fg_color="transparent")
        frame_password.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
        frame_password.grid_columnconfigure(0, weight=1)

        self.entrada_password_gerada = ctk.CTkEntry(frame_password, font=("Courier", 13), show="*")
        self.entrada_password_gerada.grid(row=0, column=0, sticky="ew")
        self.entrada_password_gerada.bind("<KeyRelease>", self.atualizar_forca_em_tempo_real)

        self.mostrar_password = False
        self.icone_eye = carregar_icone("eye.png", tamanho=20)
        self.icone_eye_off = carregar_icone("eye-off.png", tamanho=20)

        self.botao_olho = ctk.CTkButton(
            frame_password,
            text="",
            image=self.icone_eye,
            width=36,
            height=36,
            command=self.toggle_mostrar_password
        )
        self.botao_olho.grid(row=0, column=1, padx=(5, 0))

        self.label_forca = ctk.CTkProgressBar(self)
        self.label_forca.grid(row=9, column=0, padx=20, pady=(0,5), sticky="ew")
        self.label_forca.set(0)

        self.texto_forca = ctk.CTkLabel(self, text="", font=("Arial", 11))
        self.texto_forca.grid(row=10, column=0, pady=(0,10))

        ctk.CTkButton(self, text="Gerar Password", command=self.gerar).grid(row=11, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self, text="Guardar", command=self.guardar).grid(row=12, column=0, padx=20, pady=5, sticky="ew")
        ctk.CTkButton(self, text="⬅ Voltar", fg_color="transparent", border_width=2, text_color=("black", "white"), command=self.ao_voltar).grid(row=13, column=0, padx=20, pady=5, sticky="ew")

    def gerar(self):
        caracteres = ""
        if self.usar_letras.get():
            caracteres += string.ascii_letters
        if self.usar_numeros.get():
            caracteres += string.digits
        if self.usar_simbolos.get():
            caracteres += string.punctuation

        if not caracteres:
            self.texto_forca.configure(text="Escolhe pelo menos um tipo!", text_color="red")
            return

        tamanho = self.tamanho.get()
        
        self.password_gerada = "".join(random.choice(caracteres) for _ in range(tamanho))
        self.entrada_password_gerada.delete(0, "end")
        self.entrada_password_gerada.insert(0, self.password_gerada)

        forca_texto, forca_cor = self.calcular_forca(self.password_gerada)
        pontos_map = {"Fraca": 0.33, "Média": 0.66, "Forte": 1.0}
        self.label_forca.set(pontos_map[forca_texto])
        self.label_forca.configure(progress_color=forca_cor)
        self.texto_forca.configure(text=f"Força: {forca_texto}", text_color=forca_cor)

    def toggle_mostrar_password(self):
        self.mostrar_password = not self.mostrar_password
        if self.mostrar_password:
            self.entrada_password_gerada.configure(show="")
            self.botao_olho.configure(image=self.icone_eye_off)
        else:
            self.entrada_password_gerada.configure(show="*")
            self.botao_olho.configure(image=self.icone_eye)

    def limitar_descricao(self, event):
        texto = self.entrada_descricao.get()
        if len(texto) > 32:
            self.entrada_descricao.delete(32, "end")
            
    def calcular_forca(self, password):
        pontos = 0

        if len(password) >= 8:
            pontos += 1
        if len(password) >= 16:
            pontos += 1
        if any(c.islower() for c in password):
            pontos += 1
        if any(c.isupper() for c in password):
            pontos += 1
        if any(c.isdigit() for c in password):
            pontos += 1
        if any(not c.isalnum() for c in password):
            pontos += 1

        if pontos <= 2:
            return "Fraca", "red"
        elif pontos <= 4:
            return "Média", "orange"
        else:
            return "Forte", "green"

    def atualizar_forca_em_tempo_real(self, event):
        password = self.entrada_password_gerada.get()

        if not password:
            self.label_forca.set(0)
            self.texto_forca.configure(text="")
            return

        forca_texto, forca_cor = self.calcular_forca(password)
        pontos_map = {"Fraca": 0.33, "Média": 0.66, "Forte": 1.0}
        self.label_forca.set(pontos_map[forca_texto])
        self.label_forca.configure(progress_color=forca_cor)
        self.texto_forca.configure(text=f"Força: {forca_texto}", text_color=forca_cor)

    def guardar(self):
        
        self.password_gerada = self.entrada_password_gerada.get()
        if not self.password_gerada:
            self.texto_forca.configure(text="Escreve ou gera uma password!", text_color="red")
            return

        descricao = self.entrada_descricao.get()
        if not descricao:
            self.texto_forca.configure(text="Adiciona uma descrição!", text_color="red")
            return

        linhas = get_passwords(self.nome_bd, self.fernet)
        descricoes = [linha[0] for linha in linhas]

        if descricao in descricoes:
            self.texto_forca.configure(text="Já existe uma password com essa descrição!", text_color="red")
            return

        adicionar_password(self.nome_bd, self.fernet, descricao, self.password_gerada)
        self.password_gerada = ""
        self.texto_forca.configure(text="Guardado com sucesso! ✅", text_color="green")