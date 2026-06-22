import os

def get_pasta_app():
    documentos = os.path.expanduser("~\\Documents")
    pasta_app = os.path.join(documentos, "GestorPasswords")

    if not os.path.exists(pasta_app):
        os.makedirs(pasta_app)

    return pasta_app

def get_caminho(ficheiro):
    return os.path.join(get_pasta_app(), ficheiro)

def get_caminho_tema():
    return get_caminho("tema.txt")