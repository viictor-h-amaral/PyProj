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

    return dados

def Buscar_Nivel(nivel_id):
    with open(Obter_Caminho_Arquivo('Niveis.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for dado in dados:
        if dado['id'] == nivel_id: return dado

def Buscar_Niveis_Do_Usuario(usuario):
    with open(Obter_Caminho_Arquivo('Niveis.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    niveis_usuario = []
    for dado in dados:
        if dado['criador'] == usuario : niveis_usuario.append(dado)
    return niveis_usuario

def Buscar_Estrutura(estrutura_id):
    with open(Obter_Caminho_Arquivo('Estruturas.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    for dado in dados:
        if dado['id'] == estrutura_id: return dado

def Buscar_Estruturas():
    with open(Obter_Caminho_Arquivo('Estruturas.json'), 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    return dados

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
    nome_usuario = usuario['usuario']
    
    nivel_id = nivel['id']

    for user in usuarios:
        nivel_concluido = Retornar_Se_Nivel_Concluido(user, nivel_id)
        if (user['usuario'] == nome_usuario) and not nivel_concluido: 
            user['niveis_concluidos'].append(nivel['id'])
        usuarios_atualizados.append(user)
    Salvar_Usuarios(usuarios_atualizados)

def Retornar_Se_Nivel_Concluido(usuario, nivel_id):
    return (nivel_id in usuario['niveis_concluidos'])

def Salvar_Nivel(nome_nivel, dificuldade, matriz, criador):
    id_estrutura = Salvar_Estrutura(matriz)

    niveis = Buscar_Niveis()

    novo_nivel = {
        'id' : Gerar_Id(niveis), #len(niveis) + 1,
        'nome' : nome_nivel,
        'dificuldade' : dificuldade,
        'estrutura' : id_estrutura,
        'criador' : criador['usuario']
    }

    niveis.append(novo_nivel)

    with open(Obter_Caminho_Arquivo('Niveis.json'), 'w', encoding='utf-8') as f:
        json.dump(niveis, f, indent=4, ensure_ascii=False)

def Salvar_Estrutura(matriz):
    estruturas = Buscar_Estruturas()

    nova_estrutura = {
        'id' : Gerar_Id(estruturas), #len(estruturas) + 1,
        'matriz_pecas' : matriz
    }

    estruturas.append(nova_estrutura)
    with open(Obter_Caminho_Arquivo('Estruturas.json'), 'w', encoding='utf-8') as f:
        json.dump(estruturas, f, indent=4, ensure_ascii=False)

    return nova_estrutura['id']

def Gerar_Id(lista_dicionarios):
    maior_id = 0
    for dicionario in lista_dicionarios:
        if maior_id < dicionario['id']: maior_id = dicionario['id']

    return maior_id + 1
