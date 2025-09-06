import Crud as crud
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import copy

def Buscar_Proxima_Peca_Grupo(peca_id):
    grupo_peca = crud.Buscar_Grupo_Peca(peca_id)
    pecas_no_grupo = grupo_peca['pecas']
    indice_peca_atual = pecas_no_grupo.index(peca_id)

    indice_nova_peca = (indice_peca_atual + 1)%(len(pecas_no_grupo)) # y = (x+1) % comprimento_lista
    id_nova_peca = pecas_no_grupo[indice_nova_peca]

    return id_nova_peca

def Atualizar_Peca(coordenada, janela):
    botao = janela.botoes_pecas.get(coordenada)
    id_peca_atual = janela.imagens_pecas_ids[coordenada]

    id_prox_peca = Buscar_Proxima_Peca_Grupo(id_peca_atual)
    nova_imagem = Buscar_Imagem_Peca(id_prox_peca)

    janela.imagens_pecas_ids[coordenada] = id_prox_peca
    if nova_imagem not in janela.imagens_pecas:
        janela.imagens_pecas.append(nova_imagem)

    botao.config(image=nova_imagem)
    botao.image = nova_imagem

def Buscar_Imagem_Peca(peca_id):
    arquivo_img = crud.Buscar_Peca_Arquivo(peca_id)
    end_img = Endereco_Imagem(arquivo_img)

    img = Image.open(end_img)
    img = img.resize((50,50))
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
        if coordenadas_peca_atual == Coordenada_Peca_Final(matriz)  : return (True, pecas_seq_atual)
        elif len(pecas_seq_atual) == 1                              : return False
        else                                                        : return None

    for peca in lista_proximas_pecas:
        validado = Valida_Nivel(matriz, peca, copy.deepcopy(pecas_seq_atual))
        if (validado is not None) : return validado

    if len(pecas_seq_atual) == 1:
        return False

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


def Run_Tests():
    matriz1 = crud.Buscar_Estrutura_Do_Nivel(1)['matriz_pecas']
    matriz2 = crud.Buscar_Estrutura_Do_Nivel(2)['matriz_pecas']
    matriz3 = crud.Buscar_Estrutura_Do_Nivel(3)['matriz_pecas']
    matriz4 = crud.Buscar_Estrutura_Do_Nivel(4)['matriz_pecas']

    print(f'Valor esperado: TRUE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz1)}')
    print(f'Valor esperado: TRUE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz2)}')
    print(f'Valor esperado: FALSE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz3)}')
    print(f'Valor esperado: FALSE. Valor obtido: {Rotina_Verifica_Nivel_Valido(matriz4)}')

if __name__ == '__main__':
    Run_Tests()