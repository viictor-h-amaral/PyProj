from pathlib import Path
import Sys.Crud as crud
import tkinter as tk
from PIL import Image, ImageTk

Nivel = None
Estrutura = None
Matriz_Estrutural = None
controle_niveis_exibidos = [0, 10]

def Exibir_Nivel(nivel_id):

    global Nivel
    global Estrutura
    global Matriz_Estrutural

    Nivel = crud.Buscar_Nivel(nivel_id)
    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]
    
    janela_nivel = tk.Toplevel()
    janela_nivel.referencias_imagens = []

    for indice_linha, linha in enumerate(Matriz_Estrutural):
        for indice_coluna, coluna in enumerate(Matriz_Estrutural):

            peca_id = Matriz_Estrutural[indice_linha][indice_coluna]
            imagem_peca = Buscar_Imagem_Peca(peca_id)

            janela_nivel.referencias_imagens.append(imagem_peca)

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


def Gerar_Pagina_Niveis():

    pagina = tk.Toplevel()
    pagina.title("Níveis")
    pagina.geometry("800x400")

    label = tk.Label(pagina, text="Níveis", font=("Arial", 16))
    label.pack(pady=20)

    frame_niveis = tk.Frame(pagina)
    frame_niveis.pack(pady=20, fill='both', expand=True)

    frame_botoes_avancar_recuar = tk.Frame(pagina)
    frame_botoes_avancar_recuar.pack(pady=20, fill='both', expand=True)


    frame_niveis_superior = tk.Frame(frame_niveis)
    frame_niveis_superior.pack(fill='x', pady=5, expand=True)

    frame_niveis_inferior = tk.Frame(frame_niveis)
    frame_niveis_inferior.pack(fill='x', pady=5, expand=True)

    botao_recuar = tk.Button(frame_botoes_avancar_recuar, text='<', fg='white', bg='blue', 
                                        font=('Arial', 16), command=lambda: Recuar_Exibicao_Niveis(10, frame_niveis_superior, frame_niveis_inferior))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg='white', bg='red', 
                                        font=('Arial', 16), command=lambda: Avancar_Exibicao_Niveis(10, frame_niveis_superior, frame_niveis_inferior))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Niveis(frame_niveis_superior, frame_niveis_inferior)

    pagina.mainloop()

def Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf):
    for widget in frame_sup.winfo_children():
        widget.destroy()

    for widget in frame_inf.winfo_children():
        widget.destroy()

    for i in range(5):
        frame_sup.columnconfigure(i, weight=1)
        frame_inf.columnconfigure(i, weight=1)

    botoes_no_frame_superior = 0
    botoes_no_frame_inferior = 0

    niveis = crud.Buscar_Niveis()[controle_niveis_exibidos[0]:controle_niveis_exibidos[1]]

    for nivel in niveis:

        if botoes_no_frame_superior < 5:
            nivel_button = tk.Button(frame_sup, text=nivel['nome'], height=2, command=lambda p_nivelid = nivel['id']: Exibir_Nivel(p_nivelid))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(frame_inf, text=nivel['nome'], height=2, command=lambda p_nivelid = nivel['id']: Exibir_Nivel(p_nivelid))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: break

def Recuar_Exibicao_Niveis(quantidade_voltar, frame_sup, frame_inf):
    global controle_niveis_exibidos
    if (controle_niveis_exibidos[0] - quantidade_voltar < 0):
        return

    controle_niveis_exibidos[0] -= quantidade_voltar
    controle_niveis_exibidos[1] -= quantidade_voltar
    Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf)

def Avancar_Exibicao_Niveis(quantidade_avancar, frame_sup, frame_inf):
    global controle_niveis_exibidos

    quantidade_niveis_existente = len(crud.Buscar_Niveis())

    quantidade_niveis_exibidos_nesse_momento = controle_niveis_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_niveis_existente):
        return #exibir mensagem de aviso ou  no canto da tela mostrar x/x níveis

    controle_niveis_exibidos[0] += quantidade_avancar
    controle_niveis_exibidos[1] += quantidade_avancar
    Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf)