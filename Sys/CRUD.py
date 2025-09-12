import json
import os
from pathlib import Path

def Obter_Caminho_Arquivo(nome_arquivo):
    diretorio_atual = Path(__file__).parent  # Pasta Sys/
    raiz_projeto = diretorio_atual.parent    # Pasta meu_projeto/
    db_path = raiz_projeto / 'DB' / nome_arquivo
    return db_path

def Buscar_Niveis():
    with open(Obter_Caminho_Arquivo('Niveis.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    return dados['niveis']

def Buscar_Nivel(nivel_id):
    with open(Obter_Caminho_Arquivo('Niveis.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for dado in dados['niveis']:
        if dado['id'] == nivel_id: return dado

def Buscar_Niveis_Do_Usuario(usuario):
    with open(Obter_Caminho_Arquivo('Niveis.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    niveis_usuario = []
    for dado in dados['niveis']:
        if dado['criador'] == usuario : niveis_usuario.append(dado)
    return niveis_usuario

def Buscar_Estrutura(estrutura_id):
    with open(Obter_Caminho_Arquivo('Estruturas.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for dado in dados['estruturas']:
        if dado['id'] == estrutura_id: return dado

def Buscar_Estrutura_Do_Nivel(nivel_id):
    nivel = Buscar_Nivel(nivel_id)
    return Buscar_Estrutura(nivel['estrutura'])

def Carregar_Usuarios():
    with open(Obter_Caminho_Arquivo('Usuarios.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

def Carregar_Usuario(usuario):
    with open(Obter_Caminho_Arquivo('Usuarios.json'), 'r', encoding='utf-8') as f:
        dados = json.load(f)

    for dado in dados:
        if dado['usuario'] == usuario: return dado

def Salvar_Usuarios(usuarios):
    with open(Obter_Caminho_Arquivo('Usuarios.json'), 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def Buscar_Peca(peca_id):
    with open(Obter_Caminho_Arquivo('Pecas.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for dado in dados['pecas']:
        if dado['id'] == peca_id: return dado

def Buscar_Pecas():
    with open(Obter_Caminho_Arquivo('Pecas.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    pecas = []

    for dado in dados['pecas']:
        pecas.append(dado)

    return pecas

def Buscar_Peca_Arquivo(peca_id):
    peca = Buscar_Peca(peca_id)
    return peca['arquivo'] + '.png'

def Buscar_Grupo_Peca(peca_id):
    peca = Buscar_Peca(peca_id)
    grupo_id = peca['grupo_pecas']
    grupo = Buscar_Grupo_Pecas_Por_Id(grupo_id)
    return grupo

def Buscar_Grupo_Pecas_Por_Id(grupo_id):
    with open(Obter_Caminho_Arquivo('Grupos_Pecas.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for dado in dados['grupos_pecas']:
        if dado['id'] == grupo_id: return dado

def Salvar_Nivel_Concluido(usuario, nivel):
    usuarios = Carregar_Usuarios()
    usuarios_atualizados = []
    for user in usuarios:
        if user['usuario'] == usuario['usuario']: user['niveis_concluidos'].append(nivel['id'])
        usuarios_atualizados.append(user)
    Salvar_Usuarios(usuarios_atualizados)

def Retornar_Se_Nivel_Concluido(usuario, nivel_id):
    return (nivel_id in usuario['niveis_concluidos'])