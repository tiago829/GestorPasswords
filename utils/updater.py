import requests

VERSAO_ATUAL = "0.1"
URL_VERSAO = "https://raw.githubusercontent.com/tiago829/GestorPasswords/main/version.txt"
URL_DOWNLOAD = "https://github.com/tiago829/GestorPasswords/releases"

def verificar_atualizacao():
    try:
        resposta = requests.get(URL_VERSAO, timeout=5)
        versao_nova = resposta.text.strip()

        if versao_nova != VERSAO_ATUAL:
            return versao_nova
        return None
    except:
        return None