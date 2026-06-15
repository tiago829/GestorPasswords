import os
from cryptography.fernet import Fernet
from utils.paths import get_caminho


def carregar_chave():
    caminho = get_caminho("chave.key")
    if os.path.exists(caminho):
        with open(caminho, "rb") as f:
            return f.read()
    else:
        chave = Fernet.generate_key()
        with open(caminho, "wb") as f:
            f.write(chave)
        return chave


def verificar_login(fernet, password_input):
    caminho = get_caminho("config.txt")
    if not os.path.exists(caminho):
        return None, "Sem base de dados! Cria uma primeiro."

    with open(caminho, "r") as f:
        nome_bd = f.readline().strip()
        password_guardada = f.readline().strip()

    try:
        if fernet.decrypt(password_guardada.encode()).decode() != password_input:
            return None, "Password incorreta!"
    except:
        return None, "Erro ao verificar password!"

    return get_caminho(nome_bd), None
