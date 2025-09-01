from pathlib import Path
import Crud as crud
import tkinter as tk
from PIL import Image, ImageTk

Nivel = None
Estrutura = None
Matriz_Estrutural = None

def Exibir_Nivel(nivel_id):

    global Nivel
    global Estrutura
    global Matriz_Estrutural

    Nivel = crud.Buscar_Nivel(nivel_id)
    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]
    
    janela_nivel = tk.Tk()
    janela_nivel.geometry('1000x1000')

    for indice_linha, linha in enumerate(Matriz_Estrutural):
        for indice_coluna, coluna in enumerate(Matriz_Estrutural):

            peca_id = Matriz_Estrutural[indice_linha][indice_coluna]
            imagem_peca = Buscar_Imagem_Peca(peca_id)

            imagem_botao = tk.Button(janela_nivel, image=imagem_peca, 
                        command = lambda p_linha=indice_linha, p_coluna=indice_coluna: Clique_Peca(p_linha, p_coluna, peca_id))

            imagem_botao.grid(row=indice_linha, column=indice_coluna)
    janela_nivel.mainloop()

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

def Clique_Peca(linha, coluna, peca_id):
    print('clicou na peça')

Exibir_Nivel(1)