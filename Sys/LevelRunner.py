import Sys.Crud as crud
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import copy
import random

def Buscar_Proxima_Peca_Grupo(peca_id):
    grupo_peca = crud.Buscar_Grupo_Peca(peca_id)
    pecas_no_grupo = grupo_peca['pecas']
    indice_peca_atual = pecas_no_grupo.index(peca_id)

    indice_nova_peca = (indice_peca_atual + 1)%(len(pecas_no_grupo)) # y = (x+1) % comprimento_lista
    id_nova_peca = pecas_no_grupo[indice_nova_peca]

    return id_nova_peca

def Atualizar_Peca(coordenada, janela):
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
    Versão modificada da Buscar_Imagem_Peca que aceita tamanho personalizado
    """
    arquivo_img = crud.Buscar_Peca_Arquivo(peca_id)
    end_img = Endereco_Imagem(arquivo_img)
    
    img = Image.open(end_img)
    img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def Buscar_Imagem_Peca(peca_id, tamanho=None):
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
    diretorio_atual = Path(__file__).parent  # Pasta Sys/
    raiz_projeto = diretorio_atual.parent    # Pasta meu_projeto/
    img_path = raiz_projeto / 'Imgs' / 'pecas' / arquivo_imagem
    return img_path

def Rotina_Verifica_Nivel_Valido(matriz):
    return Valida_Nivel(matriz, Coordenada_Peca_Inicial(matriz), [])

def Valida_Nivel(matriz, coordenadas_peca_atual, pecas_seq_previa):
    lista_proximas_pecas = []

    if Peca_Acima_Eh_Valida      (matriz, coordenadas_peca_atual, pecas_seq_previa):  lista_proximas_pecas.append(Peca_Acima(coordenadas_peca_atual))
    if Peca_Abaixo_Eh_Valida     (matriz, coordenadas_peca_atual, pecas_seq_previa):  lista_proximas_pecas.append(Peca_Abaixo(coordenadas_peca_atual))
    if Peca_A_Esquerda_Eh_Valida (matriz, coordenadas_peca_atual, pecas_seq_previa):  lista_proximas_pecas.append(Peca_A_Esquerda(coordenadas_peca_atual))
    if Peca_A_Direita_Eh_Valida  (matriz, coordenadas_peca_atual, pecas_seq_previa):  lista_proximas_pecas.append(Peca_A_Direita(coordenadas_peca_atual))

    pecas_seq_atual = pecas_seq_previa + [coordenadas_peca_atual]

    if len(lista_proximas_pecas) == 0:
        if coordenadas_peca_atual == Coordenada_Peca_Final(matriz)      : return (True, pecas_seq_atual)
        elif coordenadas_peca_atual == Coordenada_Peca_Inicial(matriz)  : return False
        else                                                            : return None

    for peca in lista_proximas_pecas:
        validado = Valida_Nivel(matriz, peca, copy.deepcopy(pecas_seq_atual))
        if (validado is not None) : return validado

    if coordenadas_peca_atual == Coordenada_Peca_Inicial(matriz):
        return False

''' DEEPSEEK
def Valida_Nivel2(matriz, coordenadas_peca_atual, pecas_seq_previa):
    # Adiciona a peça atual ao caminho (modifica a lista original)
    pecas_seq_previa.append(coordenadas_peca_atual)
    
    # Verifica se chegou ao final
    if coordenadas_peca_atual == Coordenada_Peca_Final(matriz):
        return (True, pecas_seq_previa.copy())
    
    lista_proximas_pecas = []

    # Verifica todas as direções
    direcoes = [
        (Peca_Acima_Eh_Valida, Peca_Acima),
        (Peca_Abaixo_Eh_Valida, Peca_Abaixo),
        (Peca_A_Esquerda_Eh_Valida, Peca_A_Esquerda),
        (Peca_A_Direita_Eh_Valida, Peca_A_Direita)
    ]
    
    for validacao, movimento in direcoes:
        if validacao(matriz, coordenadas_peca_atual, pecas_seq_previa):
            lista_proximas_pecas.append(movimento(coordenadas_peca_atual))

    # Explora cada direção válida
    for peca in lista_proximas_pecas:
        resultado = Valida_Nivel(matriz, peca, pecas_seq_previa)
        if resultado is not None:
            return resultado

    # Backtrack: remove a peça atual antes de retornar
    pecas_seq_previa.pop()
    return None'''

def Peca_Acima_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    coordenadas_peca_acima = Peca_Acima(coordenadas_peca_atual)

    peca_acima_nao_existe = coordenadas_peca_acima[0] < 0
    if peca_acima_nao_existe : return False
    
    peca_acima_na_seq = coordenadas_peca_acima in pecas_seq_atual
    if peca_acima_na_seq in pecas_seq_atual : return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_acima = Retornar_Conexoes_Peca(matriz, coordenadas_peca_acima)
    sem_conexao_entre_pecas = (1 not in conexoes_peca_atual) or (3 not in conexoes_peca_acima)
    if sem_conexao_entre_pecas : return False

    return True

def Peca_Abaixo_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    coordenadas_peca_abaixo = Peca_Abaixo(coordenadas_peca_atual)
    num_linhas_nivel = len(matriz)    

    peca_abaixo_nao_existe = coordenadas_peca_abaixo[0] > num_linhas_nivel - 1
    if peca_abaixo_nao_existe : return False

    peca_abaixo_na_seq = coordenadas_peca_abaixo in pecas_seq_atual
    if peca_abaixo_na_seq : return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_abaixo = Retornar_Conexoes_Peca(matriz, coordenadas_peca_abaixo)
    sem_conexao_entre_pecas = (3 not in conexoes_peca_atual) or (1 not in conexoes_peca_abaixo)
    if sem_conexao_entre_pecas : return False

    return True

def Peca_A_Esquerda_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    coordenadas_peca_a_esquerda = Peca_A_Esquerda(coordenadas_peca_atual)
    
    peca_a_esquerda_nao_existe = coordenadas_peca_a_esquerda[1] < 0
    if peca_a_esquerda_nao_existe : return False

    peca_a_esquerda_na_seq = coordenadas_peca_a_esquerda in pecas_seq_atual
    if peca_a_esquerda_na_seq : return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_a_esquerda = Retornar_Conexoes_Peca(matriz, coordenadas_peca_a_esquerda)
    sem_conexao_entre_pecas = (4 not in conexoes_peca_atual) or (2 not in conexoes_peca_a_esquerda)
    if sem_conexao_entre_pecas : return False

    return True

def Peca_A_Direita_Eh_Valida(matriz, coordenadas_peca_atual, pecas_seq_atual):
    coordenadas_peca_a_direita = Peca_A_Direita(coordenadas_peca_atual)
    num_colunas_nivel = len(matriz[0])    

    peca_a_direita_nao_existe = coordenadas_peca_a_direita[1] > num_colunas_nivel - 1
    if peca_a_direita_nao_existe : return False

    peca_a_direita_na_seq = coordenadas_peca_a_direita in pecas_seq_atual
    if peca_a_direita_na_seq : return False

    conexoes_peca_atual = Retornar_Conexoes_Peca(matriz, coordenadas_peca_atual)
    conexoes_peca_a_direita = Retornar_Conexoes_Peca(matriz, coordenadas_peca_a_direita)
    sem_conexao_entre_pecas = (2 not in conexoes_peca_atual) or (4 not in conexoes_peca_a_direita)
    if sem_conexao_entre_pecas : return False

    return True


def Peca_Acima(coordenadas_peca_atual):
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha - 1, coluna)

def Peca_Abaixo(coordenadas_peca_atual):
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha + 1, coluna)

def Peca_A_Esquerda(coordenadas_peca_atual):
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha, coluna - 1)

def Peca_A_Direita(coordenadas_peca_atual):
    linha = coordenadas_peca_atual[0]
    coluna = coordenadas_peca_atual[1]
    return (linha, coluna + 1)

def Retornar_Conexoes_Peca(matriz, coordenadas_peca):
    peca_id = matriz[coordenadas_peca[0]][coordenadas_peca[1]]
    peca = crud.Buscar_Peca(peca_id)
    return peca['conexoes']

def Coordenada_Peca_Inicial(matriz):
    linha = len(matriz) - 1
    return (linha, 0)

def Coordenada_Peca_Final(matriz):
    coluna = len(matriz[0]) - 1
    return (0, coluna)

def Embaralhar_Pecas(matriz):
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