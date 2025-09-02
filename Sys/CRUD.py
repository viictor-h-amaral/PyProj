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

def Salvar_Usuarios(usuarios):
    with open(Obter_Caminho_Arquivo('Usuarios.json'), 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def Buscar_Peca_Arquivo(peca_id):
    with open(Obter_Caminho_Arquivo('Pecas.json'), 'r', encoding='utf-8') as f:
        dados = json.load(f)

    for peca in dados['pecas']:
        if peca['id'] == peca_id: return peca['arquivo'] + '.png'
