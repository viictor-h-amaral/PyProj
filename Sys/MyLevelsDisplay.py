from pathlib import Path
import Sys.Crud as crud
import Sys.LevelRunner as LRunner
import tkinter as tk
from Sys.Login import Obter_Usuario_Atual

Nivel = None
Estrutura = None
Matriz_Estrutural = None

controle_meus_niveis_exibidos = [0, 10]
Usuario_Atual = None

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

def Gerar_Pagina_Meus_Niveis(raiz):
    global Usuario_Atual
    Usuario_Atual = Obter_Usuario_Atual()

    pagina = tk.Toplevel(raiz)
    pagina.transient(raiz)
    pagina.grab_set()
    pagina.focus_force()
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