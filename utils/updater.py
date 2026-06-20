import requests
import os
from utils.paths import get_pasta_app

URL_VERSAO = "https://raw.githubusercontent.com/tiago829/GestorPasswords/main/version.txt"
URL_DOWNLOAD = "https://github.com/tiago829/GestorPasswords/releases"


def get_versao_atual():
    # Lê o version.txt que vem empacotado no .exe
    import sys
    if hasattr(sys, "_MEIPASS"):
        caminho = os.path.join(sys._MEIPASS, "version.txt")
    else:
        caminho = "version.txt"

    with open(caminho, "r") as f:
        return f.read().strip()


def verificar_atualizacao():
    try:
        versao_atual = get_versao_atual()
        resposta = requests.get(URL_VERSAO, timeout=5)
        versao_nova = resposta.text.strip()
        print(f"DEBUG: local='{versao_atual}' github='{versao_nova}'")

        if versao_nova != versao_atual:
            return versao_nova
        return None
    except:
        print(f"DEBUG erro: {e}")
        return None