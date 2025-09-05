import Sys.Crud as crud
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

def Buscar_Proxima_Peca_Grupo(peca_id):
    grupo_peca = crud.Buscar_Grupo_Peca(peca_id)
    pecas_no_grupo = grupo_peca['pecas']
    indice_peca_atual = pecas_no_grupo.index(peca_id)

    indice_nova_peca = (indice_peca_atual + 1)%(len(pecas_no_grupo)) # y = (x+1) % comprimento_lista
    id_nova_peca = pecas_no_grupo[indice_nova_peca]

    return id_nova_peca

def Clique_Peca(coordenada, janela):
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