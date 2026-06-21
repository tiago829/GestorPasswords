import customtkinter as ctk
from PIL import Image, ImageOps
import os

PASTA_ASSETS = "assets"


def criar_versao_branca(imagem):
    # Mantém o canal alpha (transparência) e inverte só as cores para branco
    r, g, b, a = imagem.split()
    branco = Image.new("RGBA", imagem.size, (255, 255, 255, 0))
    branco.putalpha(a)
    return branco


def carregar_icone(nome, tamanho=20):
    caminho = os.path.join(PASTA_ASSETS, nome)
    imagem_preta = Image.open(caminho).convert("RGBA")
    imagem_branca = criar_versao_branca(imagem_preta)

    return ctk.CTkImage(
        light_image=imagem_branca,
        dark_image=imagem_preta,
        size=(tamanho, tamanho)
    )
