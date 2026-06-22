import customtkinter as ctk
import os
from utils.paths import get_caminho_tema


class SettingsView(ctk.CTkFrame):
    def __init__(self, parent, ao_voltar):
        super().__init__(parent)
        self.ao_voltar = ao_voltar

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="⚙️ Definições", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=20)

        ctk.CTkLabel(self, text="Tema:", font=("Arial", 13)).grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        # Lê o tema guardado, se existir
        caminho = get_caminho_tema()
        if os.path.exists(caminho):
            with open(caminho, "r") as f:
                tema_guardado = f.read().strip()
        else:
            tema_guardado = "Dark"

        self.opcao_tema = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light", "System"],
            command=self.mudar_tema
        )
        self.opcao_tema.set(tema_guardado)
        self.opcao_tema.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkButton(
            self,
            text="⬅ Voltar",
            fg_color="transparent",
            border_width=2,
            text_color=("black", "white"),
            command=self.ao_voltar
        ).grid(row=3, column=0, padx=20, pady=20, sticky="ew")

    def mudar_tema(self, escolha):
        print(f"Tema escolhido: {escolha}")
        print(f"A guardar em: {get_caminho_tema()}")
        ctk.set_appearance_mode(escolha)
        with open(get_caminho_tema(), "w") as f:
            f.write(escolha)
        print("Guardado!")