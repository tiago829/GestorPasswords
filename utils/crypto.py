def encriptar(nome_bd, fernet):
    with open(nome_bd, "rb") as f:
        dados = f.read()
    with open(nome_bd, "wb") as f:
        f.write(fernet.encrypt(dados))


def desencriptar(nome_bd, fernet):
    with open(nome_bd, "rb") as f:
        dados = f.read()
    with open(nome_bd, "wb") as f:
        f.write(fernet.decrypt(dados))
