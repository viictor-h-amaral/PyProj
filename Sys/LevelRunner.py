"""
Módulo de execução e validação de níveis.

Contém a lógica principal para manipulação de peças, validação de caminhos
e execução dos níveis do jogo.
"""

import Sys.Crud as crud
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import copy
import random


def Buscar_Proxima_Peca_Grupo(peca_id):
    """
    Busca a próxima peça no grupo da peça atual (rotação cíclica).
    
    Args:
        peca_id: ID da peça atual
        
    Returns:
        int: ID da próxima peça no grupo
    """
    grupo_peca = crud.Buscar_Grupo_Peca(peca_id)
    pecas_no_grupo = grupo_peca['pecas']
    indice_peca_atual = pecas_no_grupo.index(peca_id)

    indice_nova_peca = (indice_peca_atual + 1) % (len(pecas_no_grupo))
    id_nova_peca = pecas_no_grupo[indice_nova_peca]

    return id_nova_peca


def Atualizar_Peca(coordenada, janela):
    """
    Atualiza a peça na coordenada especificada para a próxima do grupo.
    
    Args:
        coordenada: Tupla (linha, coluna) da peça
        janela: Janela contendo os botões das peças
    """
    botao = janela.botoes_pecas.get(coordenada)
    if not botao:
        return
        
    id_peca_atual = janela.pecas_ids[coordenada[0]][coordenada[1]]
    id_prox_peca = Buscar_Proxima_Peca_Grupo(id_peca_atual)
    
    # Obtém o tamanho atual da imagem do botão
    if hasattr(botao, 'image') and botao.image:
        # Usa o mesmo tamanho da imagem atual
        tamanho_atual = (botao.image.width(), botao.image.height())
        nova_imagem = Buscar_Imagem_Peca(id_prox_peca, tamanho_atual)
    else:
        # Se não tem imagem, usa tamanho padrão (fallback)
        nova_imagem = Buscar_Imagem_Peca(id_prox_peca)
    
    # Atualiza o ID da peça
    janela.pecas_ids[coordenada[0]][coordenada[1]] = id_prox_peca
    
    # Atualiza a imagem
    botao.config(image=nova_imagem)
    botao.image = nova_imagem
    
    # Adiciona à lista de imagens se não estiver lá
    if nova_imagem not in janela.imagens_pecas:
        janela.imagens_pecas.append(nova_imagem)


def Buscar_Imagem_Peca_Redimensionada(peca_id, tamanho):
    """
    Busca imagem de peça redimensionada para tamanho personalizado.
    
    Args:
        peca_id: ID da peça
        tamanho: Tamanho desejado para a imagem
        
    Returns:
        ImageTk.PhotoImage: Imagem redimensionada
    """
    arquivo_img = crud.Buscar_Peca_Arquivo(peca_id)
    end_img = Endereco_Imagem(arquivo_img)
    
    img = Image.open(end_img)
    img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)


def Buscar_Imagem_Peca(peca_id, tamanho=None):
    """
    Busca imagem da peça com opção de redimensionamento.
    
    Args:
        peca_id: ID da peça
        tamanho: Tamanho opcional (largura, altura)
        
    Returns:
        ImageTk.PhotoImage: Imagem da peça
    """
    arquivo_img = crud.Buscar_Peca_Arquivo(peca_id)
    end_img = Endereco_Imagem(arquivo_img)

    img = Image.open(end_img)
    
    # Se não especificar tamanho, usa tamanho padrão de 80x80
    if tamanho is None:
        img = img.resize((80, 80), Image.Resampling.LANCZOS)
    else:
        img = img.resize(tamanho, Image.Resampling.LANCZOS)
    
    return ImageTk.PhotoImage(img)


def Endereco_Imagem(arquivo_imagem):
    """
    Retorna o caminho completo para uma imagem de peça.
    
    Args:
        arquivo_imagem: Nome do arquivo da imagem
        
    Returns:
        Path: Caminho completo para a imagem
    """
    diretorio_atual = Path(__file__).parent  # Pasta Sys/
    raiz_projeto = diretorio_atual.parent    # Pasta meu_projeto/
    img_path = raiz_projeto / 'Imgs' / 'pecas' / arquivo_imagem
    return img_path


def Rotina_Verifica_Nivel_Valido(matriz):
    """
    Inicia a rotina de validação do nível.
    
    Args:
        matriz: Matriz representando o nível
        
    Returns:
        bool: True se o nível for válido, False caso contrário
    """
    return Valida_Nivel(matriz, Coordenada_Peca_Inicial(matriz), [])


def Valida_Nivel(matriz, coordenadas_peca_atual, pecas_seq_previa):
    """
    Função recursiva para validar se o nível tem um caminho válido.
    
    Args:
        matriz: Matriz do nível
        coordenadas_peca_atual: Coordenadas da peça atual sendo validada
        pecas_seq_previa: Lista de peças já visitadas na sequência
        
    Returns:
        bool/None: True se válido, False se inválido, None se caminho incompleto
    """
    lista_proximas_pecas = []

    if Peca_Acima_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_previa):  
        lista_proximas_pecas.append(Peca_Acima(coordenadas_peca_atual))
    if Peca_Abaixo_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_previa):  
        lista_proximas_pecas.append(Peca_Abaixo(coordenadas_peca_atual))
    if Peca_A_Esquerda_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_previa):  
        lista_proximas_pecas.append(Peca_A_Esquerda(coordenadas_peca_atual))
    if Peca_A_Direita_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_previa):  
        lista_proximas_pecas.append(Peca_A_Direita(coordenadas_peca_atual))

    pecas_seq_atual = pecas_seq_previa + [coordenadas_peca_atual]

    if len(lista_proximas_pecas) == 0:
        if coordenadas_peca_atual == Coordenada_Peca_Final(matriz):      
            return (True, pecas_seq_atual)
        elif coordenadas_peca_atual == Coordenada_Peca_Inicial(matriz):  
            return False
        else:                                                            
            return None

    for peca in lista_proximas_pecas:
        validado = Valida_Nivel(matriz, peca, copy.deepcopy(pecas_seq_atual))
        if (validado is not None): 
            return validado

    if coordenadas_peca_atual == Coordenada_Peca_Inicial(matriz):
        return False


def Peca_Acima_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    """
    Verifica se a peça acima é válida para conexão.
    
    Args:
        matriz: Matriz do nível
        coordenadas_peca_atual: Coordenadas da peça atual
        pecas_seq_atual: Lista de peças visitadas
        
    Returns:
        bool: True se a peça acima for válida
    """
    coordenadas_peca_acima = Peca_Acima(coordenadas_peca_atual)

    peca_acima_nao_existe = coordenadas_peca_acima[0] < 0
    if peca_acima_nao_existe: 
        return False
    
    peca_acima_na_seq = coordenadas_peca_acima in pecas_seq_atual
    if peca_acima_na_seq: 
        return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_acima = Retornar_Conexoes_Peca(matriz, coordenadas_peca_acima)
    sem_conexao_entre_pecas = (1 not in conexoes_peca_atual) or (3 not in conexoes_peca_acima)
    if sem_conexao_entre_pecas: 
        return False

    return True


def Peca_Abaixo_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    """
    Verifica se a peça abaixo é válida para conexão.
    
    Args:
        matriz: Matriz do nível
        coordenadas_peca_atual: Coordenadas da peça atual
        pecas_seq_atual: Lista de peças visitadas
        
    Returns:
        bool: True se a peça abaixo for válida
    """
    coordenadas_peca_abaixo = Peca_Abaixo(coordenadas_peca_atual)
    num_linhas_nivel = len(matriz)    

    peca_abaixo_nao_existe = coordenadas_peca_abaixo[0] > num_linhas_nivel - 1
    if peca_abaixo_nao_existe: 
        return False

    peca_abaixo_na_seq = coordenadas_peca_abaixo in pecas_seq_atual
    if peca_abaixo_na_seq: 
        return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_abaixo = Retornar_Conexoes_Peca(matriz, coordenadas_peca_abaixo)
    sem_conexao_entre_pecas = (3 not in conexoes_peca_atual) or (1 not in conexoes_peca_abaixo)
    if sem_conexao_entre_pecas: 
        return False

    return True


def Peca_A_Esquerda_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    """
    Verifica se a peça à esquerda é válida para conexão.
    
    Args:
        matriz: Matriz do nível
        coordenadas_peca_atual: Coordenadas da peça atual
        pecas_seq_atual: Lista de peças visitadas
        
    Returns:
        bool: True se a peça à esquerda for válida
    """
    coordenadas_peca_a_esquerda = Peca_A_Esquerda(coordenadas_peca_atual)
    
    peca_a_esquerda_nao_existe = coordenadas_peca_a_esquerda[1] < 0
    if peca_a_esquerda_nao_existe: 
        return False

    peca_a_esquerda_na_seq = coordenadas_peca_a_esquerda in pecas_seq_atual
    if peca_a_esquerda_na_seq: 
        return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_a_esquerda = Retornar_Conexoes_Peca(matriz, coordenadas_peca_a_esquerda)
    sem_conexao_entre_pecas = (4 not in conexoes_peca_atual) or (2 not in conexoes_peca_a_esquerda)
    if sem_conexao_entre_pecas: 
        return False

    return True


def Peca_A_Direita_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    """
    Verifica se a peça à direita é válida para conexão.
    
    Args:
        matriz: Matriz do nível
        coordenadas_peca_atual: Coordenadas da peça atual
        pecas_seq_atual: Lista de peças visitadas
        
    Returns:
        bool: True se a peça à direita for válida
    """
    coordenadas_peca_a_direita = Peca_A_Direita(coordenadas_peca_atual)
    num_colunas_nivel = len(matriz[0])    

    peca_a_direita_nao_existe = coordenadas_peca_a_direita[1] > num_colunas_nivel - 1
    if peca_a_direita_nao_existe: 
        return False

    peca_a_direita_na_seq = coordenadas_peca_a_direita in pecas_seq_atual
    if peca_a_direita_na_seq: 
        return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_a_direita = Retornar_Conexoes_Peca(matriz, coordenadas_peca_a_direita)
    sem_conexao_entre_pecas = (2 not in conexoes_peca_atual) or (4 not in conexoes_peca_a_direita)
    if sem_conexao_entre_pecas: 
        return False

    return True


def Peca_Acima(coordenadas_peca_atual):
    """
    Retorna coordenadas da peça acima.
    
    Args:
        coordenadas_peca_atual: Coordenadas atuais (linha, coluna)
        
    Returns:
        tuple: Coordenadas da peça acima
    """
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha - 1, coluna)


def Peca_Abaixo(coordenadas_peca_atual):
    """
    Retorna coordenadas da peça abaixo.
    
    Args:
        coordenadas_peca_atual: Coordenadas atuais (linha, coluna)
        
    Returns:
        tuple: Coordenadas da peça abaixo
    """
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha + 1, coluna)


def Peca_A_Esquerda(coordenadas_peca_atual):
    """
    Retorna coordenadas da peça à esquerda.
    
    Args:
        coordenadas_peca_atual: Coordenadas atuais (linha, coluna)
        
    Returns:
        tuple: Coordenadas da peça à esquerda
    """
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha, coluna - 1)


def Peca_A_Direita(coordenadas_peca_atual):
    """
    Retorna coordenadas da peça à direita.
    
    Args:
        coordenadas_peca_atual: Coordenadas atuais (linha, coluna)
        
    Returns:
        tuple: Coordenadas da peça à direita
    """
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha, coluna + 1)


def Retornar_Conexoes_Peca(matriz, coordenadas_peca):
    """
    Retorna as conexões de uma peça específica.
    
    Args:
        matriz: Matriz do nível
        coordenadas_peca: Coordenadas da peça
        
    Returns:
        list: Lista de conexões da peça"""

    peca_id = matriz[coordenadas_peca[0]][coordenadas_peca[1]]
    peca = crud.Buscar_Peca(peca_id)
    return peca['conexoes']

def Coordenada_Peca_Inicial(matriz):
    """
    Retorna as coordenadas da peça inicial da matriz estrutural dada.
    
    Args:
        matriz: Matriz do nível
        
    Returns:
        tuple: Tupla contendo as coordenadas da primeira peça da estrutura (linha, coluna)"""

    linha = len(matriz) - 1
    return (linha, 0)

def Coordenada_Peca_Final(matriz):
    """
    Retorna as coordenadas da peça final da matriz estrutural dada.
    
    Args:
        matriz: Matriz do nível
        
    Returns:
        tuple: Tupla contendo as coordenadas da última peça da estrutura (linha, coluna)"""

    coluna = len(matriz[0]) - 1
    return (0, coluna)

def Embaralhar_Pecas(matriz):
    """
    Retorna uma matriz estrutural cuja peça (i, j) é alguma peça pertence ao grupo de peças da peça (i, j)
    da matriz fornecida. Ou seja, embaralha as peças, concervando sempre os grupos das peças originais.
    
    Args:
        matriz: Matriz do nível
        
    Returns:
        list[list]: Lista aninhada contendo as peças da matriz estrutural embaralhadas"""

    matriz_embaralhada = copy.deepcopy(matriz)
    for indice_linha, linha in enumerate(matriz):
        for indice_coluna, coluna in enumerate(linha):

            peca_original_id = matriz[indice_linha][indice_coluna]
            grupo_peca = crud.Buscar_Grupo_Peca(peca_original_id)
            pecas_no_grupo = grupo_peca['pecas']

            matriz_embaralhada[indice_linha][indice_coluna] = random.choice(pecas_no_grupo)

    return matriz_embaralhada

def Run_Tests():
    matriz1 = [[13, 23],
               [26, 41]]

    matriz2 = [[23, 22, 22, 22],
                [21, 23, 14, 0],
                [21, 34, 14, 0],
                [26, 33, 14, 0]]

    matriz3 = [[23, 22, 0, 22],
               [21, 23, 14, 0],
               [21, 34, 14, 0],
               [26, 33, 14, 0]]

    matriz4 = [[23, 21, 0, 22],
               [22, 26, 13, 0],
               [22, 33, 13, 0],
               [25, 32, 13, 0]]

    print(f'Valor esperado: TRUE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz1)}')
    print(f'Valor esperado: TRUE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz2)}')
    print(f'Valor esperado: FALSE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz3)}')
    print(f'Valor esperado: FALSE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz4)}')

if __name__ == '__main__':
    Run_Tests()