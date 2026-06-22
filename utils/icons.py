import customtkinter as ctk
from PIL import Image
import os
import sys


def get_pasta_assets():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "assets")
    return "assets"


def carregar_icone(nome, tamanho=20):
    caminho = os.path.join(get_pasta_assets(), nome)
    imagem = Image.open(caminho).convert("RGBA")

    # Versão branca — mantém transparência mas pinta tudo de branco
    r, g, b, a = imagem.split()
    branca = Image.new("RGBA", imagem.size, (255, 255, 255, 255))
    branca.putalpha(a)

    # Versão preta — usa a imagem original (já é preta)
    preta = imagem

    return ctk.CTkImage(
        light_image=preta,   # tema claro → ícone preto
        dark_image=branca,   # tema escuro → ícone branco
        size=(tamanho, tamanho)
    )