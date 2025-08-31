import hashlib

def Codificar_Senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def Descodificar_Senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()