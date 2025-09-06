from pathlib import Path
import Sys.Crud as crud
import Sys.LevelRunner as LRunner
import tkinter as tk
from tkinter import messagebox
import copy

#region VARS_GLOBAIS

Nivel = None
Estrutura = None
Matriz_Estrutural = None
controle_niveis_exibidos = [0, 10]

controle_meus_niveis_exibidos = [0, 10]
Usuario_Atual = None

Nivel_Atual_Concluido = False

#endregion VARS_GLOBAIS

#region NIVEIS

def Exibir_Nivel(nivel_id):

    global Nivel
    global Estrutura
    global Matriz_Estrutural
    global Nivel_Atual_Concluido

    Nivel = crud.Buscar_Nivel(nivel_id)
    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]
    
    raiz = tk.Toplevel()

    raiz.rowconfigure(0, weight=1)

    for i in range(2):
        raiz.columnconfigure(i, weight=1)

    frame_esquerda = tk.Frame(raiz)
    janela_nivel = tk.Frame(raiz)
    frame_direita = tk.Frame(raiz)

    frame_esquerda.grid(row=0, column=0, sticky='nsew')
    janela_nivel.grid(row=0, column=1, sticky='nsew')
    frame_direita.grid(row=0, column=2, sticky='nsew')

    frame_esquerda.columnconfigure(0, weight=1)
    frame_direita.columnconfigure(0, weight=1)

    for i in range(len(Matriz_Estrutural)):
        frame_esquerda.rowconfigure(i, weight=1)
        frame_direita.rowconfigure(i, weight=1)

    tk.Label(frame_esquerda, text="Início", font=("Arial", 16)).grid(column=0, row=(len(Matriz_Estrutural) - 1), sticky='s', pady=10)
    tk.Label(frame_direita, text="Fim", font=("Arial", 16)).grid(column=0, row=0, sticky='n', pady=10)

    janela_nivel.botoes_pecas = {}
    janela_nivel.pecas_ids = []
    janela_nivel.imagens_pecas = []

    for indice_linha, linha in enumerate(Matriz_Estrutural):
        for indice_coluna, coluna in enumerate(Matriz_Estrutural):

            peca_id = Matriz_Estrutural[indice_linha][indice_coluna]
            janela_nivel.pecas_ids = copy.deepcopy(Matriz_Estrutural)

            imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id)
            if imagem_peca not in janela_nivel.imagens_pecas: janela_nivel.imagens_pecas.append(imagem_peca)

            imagem_botao = tk.Button(janela_nivel, image=imagem_peca, 
                        command = lambda p_linha=indice_linha, p_coluna=indice_coluna: Rotina_Clique_Peca((p_linha, p_coluna), janela_nivel))

            imagem_botao.grid(row=indice_linha, column=indice_coluna)

            janela_nivel.botoes_pecas[(indice_linha, indice_coluna)] = imagem_botao

    Nivel_Atual_Concluido = LRunner.Rotina_Verifica_Nivel_Valido(Matriz_Estrutural)
    raiz.mainloop()

def Rotina_Clique_Peca(coordenada, janela_nivel):
    LRunner.Atualizar_Peca(coordenada, janela_nivel)
    Rotina_Valida_Nivel(janela_nivel.pecas_ids)
    
def Rotina_Valida_Nivel(matriz):
    global Nivel_Atual_Concluido

    nivel_concluido = LRunner.Rotina_Verifica_Nivel_Valido(matriz)
    if nivel_concluido: 
        if (not Nivel_Atual_Concluido) : messagebox.showinfo("Sucesso", "Nível concluído!")
        Nivel_Atual_Concluido = True
    else: Nivel_Atual_Concluido = False

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

    todos_niveis = crud.Buscar_Niveis()
    niveis = todos_niveis[controle_niveis_exibidos[0]:controle_niveis_exibidos[1]]

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
        return

    controle_niveis_exibidos[0] += quantidade_avancar
    controle_niveis_exibidos[1] += quantidade_avancar
    Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf)

#endregion NIVEIS

#region MEUS_NIVEIS

def Exibir_Meu_Nivel(nivel_id):

    global Nivel
    global Estrutura
    global Matriz_Estrutural

    Nivel = crud.Buscar_Nivel(nivel_id)
    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]
    
    janela_nivel = tk.Toplevel()
    janela_nivel.botoes_pecas = {}
    janela_nivel.pecas_ids = {}
    janela_nivel.imagens_pecas = []

    for indice_linha, linha in enumerate(Matriz_Estrutural):
        for indice_coluna, coluna in enumerate(Matriz_Estrutural):

            peca_id = Matriz_Estrutural[indice_linha][indice_coluna]
            janela_nivel.pecas_ids[(indice_linha, indice_coluna)] = peca_id

            imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id)
            janela_nivel.imagens_pecas.append(imagem_peca)

            imagem_botao = tk.Button(janela_nivel, image=imagem_peca)

            imagem_botao.grid(row=indice_linha, column=indice_coluna)

            janela_nivel.botoes_pecas[(indice_linha, indice_coluna)] = imagem_botao

    janela_nivel.mainloop()

def Gerar_Pagina_Meus_Niveis(usuario):
    global Usuario_Atual
    Usuario_Atual = usuario

    pagina = tk.Toplevel()
    pagina.title("Meus níveis")
    pagina.geometry("800x400")

    label = tk.Label(pagina, text="Meu níveis", font=("Arial", 16))
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
                                        font=('Arial', 16), command=lambda: Recuar_Exibicao_Meus_Niveis(10, frame_niveis_superior, frame_niveis_inferior))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg='white', bg='red', 
                                        font=('Arial', 16), command=lambda: Avancar_Exibicao_Meus_Niveis(10, frame_niveis_superior, frame_niveis_inferior))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior)

    pagina.mainloop()

def Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf):
    for widget in frame_sup.winfo_children():
        widget.destroy()

    for widget in frame_inf.winfo_children():
        widget.destroy()

    for i in range(5):
        frame_sup.columnconfigure(i, weight=1)
        frame_inf.columnconfigure(i, weight=1)

    botoes_no_frame_superior = 0
    botoes_no_frame_inferior = 0

    todos_niveis = crud.Buscar_Niveis_Do_Usuario(Usuario_Atual['usuario'])
    niveis = todos_niveis[controle_meus_niveis_exibidos[0]:controle_meus_niveis_exibidos[1]]

    for nivel in niveis:

        if botoes_no_frame_superior < 5:
            nivel_button = tk.Button(frame_sup, text=nivel['nome'], height=2, command=lambda p_nivelid = nivel['id']: Exibir_Meu_Nivel(p_nivelid))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(frame_inf, text=nivel['nome'], height=2, command=lambda p_nivelid = nivel['id']: Exibir_Meu_Nivel(p_nivelid))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: break

def Avancar_Exibicao_Meus_Niveis(quantidade_avancar, frame_sup, frame_inf):
    global controle_meus_niveis_exibidos

    quantidade_niveis_existente = len(crud.Buscar_Niveis_Do_Usuario(Usuario_Atual['usuario']))

    quantidade_niveis_exibidos_nesse_momento = controle_meus_niveis_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_niveis_existente):
        return

    controle_meus_niveis_exibidos[0] += quantidade_avancar
    controle_meus_niveis_exibidos[1] += quantidade_avancar
    Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf)

def Recuar_Exibicao_Meus_Niveis(quantidade_voltar, frame_sup, frame_inf):
    global controle_meus_niveis_exibidos
    if (controle_meus_niveis_exibidos[0] - quantidade_voltar < 0):
        return

    controle_meus_niveis_exibidos[0] -= quantidade_voltar
    controle_meus_niveis_exibidos[1] -= quantidade_voltar
    Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf)


#endregion MEUS_NIVEIS