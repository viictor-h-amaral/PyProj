from pathlib import Path
import Sys.Crud as crud
import Sys.LevelRunner as LRunner
import tkinter as tk
from Sys.Login import Obter_Usuario_Atual, Centralizar_Janela
from tkinter import messagebox
import Sys.Codifier as codifier

Nivel = None
Estrutura = None
Matriz_Estrutural = None

controle_meus_niveis_exibidos = [0, 10]
Usuario_Atual = None

def Exibir_Meu_Nivel(nivel_id, pagina, frame_sup, frame_inf):

    global Nivel
    global Estrutura
    global Matriz_Estrutural

    Nivel = crud.Buscar_Nivel(nivel_id)
    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]

    largura_janela, altura_janela, tamanho_celula = Calcular_Tamanho_Janela(Matriz_Estrutural)

    janela_nivel = tk.Toplevel(pagina)
    janela_nivel.transient(pagina)
    janela_nivel.grab_set()
    janela_nivel.focus_force()

    def ao_fechar_meu_nivel():
        janela_nivel.destroy()
        pagina.focus_force()
        pagina.grab_set()
    
    janela_nivel.protocol("WM_DELETE_WINDOW", ao_fechar_meu_nivel)

    janela_nivel.title(f"Nível Concluído {nivel_id}")
    janela_nivel.geometry(f'{largura_janela}x{altura_janela}')
    janela_nivel.resizable(False, False)
    Centralizar_Janela(janela_nivel)

    num_linhas = len(Matriz_Estrutural)
    num_colunas = len(Matriz_Estrutural[0])
    
    # Configuração similar
    janela_nivel.grid_rowconfigure(0, weight=1)
    janela_nivel.grid_columnconfigure(1, weight=1)
    
    frame_esquerda = tk.Frame(janela_nivel, width=100)
    frame_direita = tk.Frame(janela_nivel, width=100)
    
    # Frame principal para o nível
    frame_nivel = tk.Frame(janela_nivel)
    
    frame_esquerda.grid(row=0, column=0, sticky='ns')
    frame_nivel.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
    frame_direita.grid(row=0, column=2, sticky='ns')
    
    for i in range(num_linhas):
        frame_nivel.grid_rowconfigure(i, weight=1, uniform="peca_row")
    for j in range(num_colunas):
        frame_nivel.grid_columnconfigure(j, weight=1, uniform="peca_col")
    
    tk.Label(frame_esquerda, text="Início", font=("Arial", 14), fg='green').pack(side='bottom', pady=10)

    def Apagar_Nivel():
        def Limpar_Pagina_Meus_Niveis():
            Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, pagina)
            janela_nivel.destroy()

        Exibir_Janela_Apagar_Nivel(pagina, nivel_id, lambda: Limpar_Pagina_Meus_Niveis())

    tk.Button(frame_esquerda, text="Apagar nível", font=("Arial", 14), bg='red', fg='white',
                            command=lambda: Apagar_Nivel()).pack(side='top', pady=10)

    tk.Label(frame_direita, text="Fim", font=("Arial", 14), fg='red').pack(side='top', pady=10)

    frame_nivel.botoes_pecas = {}
    frame_nivel.pecas_ids = {}
    frame_nivel.imagens_pecas = []

    botoes = {}
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):
            botao = tk.Button(frame_nivel, state='disabled')
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            botoes[(indice_linha, indice_coluna)] = botao

    def atualizar_imagens_meu_nivel():
        if botoes:
            primeiro_botao = list(botoes.values())[0]
            primeiro_botao.update_idletasks()
            largura_botao = primeiro_botao.winfo_width()
            altura_botao = primeiro_botao.winfo_height()
            
            tamanho_imagem = min(largura_botao, altura_botao) - 2
            
            for (linha, coluna), botao in botoes.items():
                peca_id = Matriz_Estrutural[linha][coluna]
                imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
                frame_nivel.imagens_pecas.append(imagem_peca)
                botao.config(image=imagem_peca, state='normal')
                botao.image = imagem_peca

    janela_nivel.after(100, atualizar_imagens_meu_nivel)
    janela_nivel.mainloop()

def Gerar_Pagina_Meus_Niveis(raiz):
    global Usuario_Atual
    Usuario_Atual = Obter_Usuario_Atual()

    pagina = tk.Toplevel(raiz)
    pagina.transient(raiz)
    pagina.grab_set()
    pagina.focus_force()

    def ao_fechar_pagina_niveis():
        pagina.destroy()
        raiz.focus_force()
        raiz.grab_release()  # Libera o grab da janela principal
    
    pagina.protocol("WM_DELETE_WINDOW", ao_fechar_pagina_niveis)

    pagina.title("Meus níveis")
    pagina.geometry("800x400")

    Centralizar_Janela(pagina)

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

    botao_recuar = tk.Button(frame_botoes_avancar_recuar, text='<', fg='white', bg='#3b68ff', 
                                        font=('Arial', 16), command=lambda: Recuar_Exibicao_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg='white', bg='#ff3b3b', 
                                        font=('Arial', 16), command=lambda: Avancar_Exibicao_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina)

    pagina.mainloop()

def Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, janela_niveis):
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
        bg = 'white'
        fg = 'black'
        match (nivel['dificuldade'].upper()):
            case 'FACIL': bg = '#a3ffa8' 
            case 'MEDIO': bg = '#fcffa3'
            case 'DIFICIL': bg = '#ff8787'

        if botoes_no_frame_superior < 5:
            nivel_button = tk.Button(frame_sup, text=nivel['nome'], height=2, bg=bg, fg=fg, font=('Arial', 9, 'bold'),
                                    command=lambda p_nivelid = nivel['id']: Exibir_Meu_Nivel(p_nivelid, janela_niveis, frame_sup, frame_inf))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(frame_inf, text=nivel['nome'], height=2, bg=bg, fg=fg, font=('Arial', 9, 'bold'),
                                    command=lambda p_nivelid = nivel['id']: Exibir_Meu_Nivel(p_nivelid, janela_niveis, frame_sup, frame_inf))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: break

def Avancar_Exibicao_Meus_Niveis(frame_sup, frame_inf, janela_raiz):
    global controle_meus_niveis_exibidos

    quantidade_niveis_existente = len(crud.Buscar_Niveis_Do_Usuario(Usuario_Atual['usuario']))

    quantidade_niveis_exibidos_nesse_momento = controle_meus_niveis_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_niveis_existente):
        return

    controle_meus_niveis_exibidos[0] += 10
    controle_meus_niveis_exibidos[1] += 10
    Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, janela_raiz)

def Recuar_Exibicao_Meus_Niveis(frame_sup, frame_inf, janela_raiz):
    global controle_meus_niveis_exibidos
    if (controle_meus_niveis_exibidos[0] - 10 < 0):
        return

    controle_meus_niveis_exibidos[0] -= 10
    controle_meus_niveis_exibidos[1] -= 10
    Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, janela_raiz)

def Calcular_Tamanho_Janela(matriz):
    """
    Calcula o tamanho ideal da janela baseado na matriz
    Mantém peças maiores para matrizes pequenas e ajusta para matrizes grandes
    """
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])
    
    # Tamanho base por célula (ajuste esses valores conforme necessário)
    if num_linhas <= 3 and num_colunas <= 3:
        tamanho_celula = 120  # Matrizes pequenas: peças grandes
    elif num_linhas <= 5 and num_colunas <= 5:
        tamanho_celula = 90   # Matrizes médias: peças médias
    else:
        tamanho_celula = 70   # Matrizes grandes: peças menores
    
    # Calcula tamanho total da área do nível
    largura_nivel = num_colunas * tamanho_celula
    altura_nivel = num_linhas * tamanho_celula
    
    # Adiciona espaço para as labels "Início" e "Fim" e margens
    largura_total = largura_nivel + 200  # +200 para labels laterais e margens
    altura_total = altura_nivel + 100    # +100 para margens superior e inferior
    
    return largura_total, altura_total, tamanho_celula

def Exibir_Janela_Apagar_Nivel(raiz, nivel_id, callback = None):
    janela_confirmacao = tk.Toplevel(raiz)
    janela_confirmacao.transient(raiz)
    janela_confirmacao.grab_set()
    janela_confirmacao.focus_force()

    def ao_fechar_janela():
        janela_confirmacao.destroy()
        raiz.grab_set()
        raiz.focus_force()

    janela_confirmacao.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    def Excluir_Nivel():
        senha = senha_entry.get()
        if not senha or codifier.Codificar_Senha(senha) != Obter_Usuario_Atual()['senha']:
            messagebox.showerror("Opss", "Senha incorreta!")
            return
        crud.Excluir_Nivel(nivel_id)
        messagebox.showinfo("Sucesso", "Nível excluído com sucesso!")
        ao_fechar_janela()
        if callback:
            callback()

    tk.Label(janela_confirmacao, text='Confirme sua senha: ').grid(row=0, column=0, padx=5, pady=5)
    senha_entry = tk.Entry(janela_confirmacao, show='*')
    senha_entry.grid(row=0, column=1, padx=5, pady=5)
    senha_entry.focus()
    senha_entry.bind('<Return>', lambda e: Excluir_Nivel())

    tk.Button(janela_confirmacao, text='Cancelar', command=lambda: ao_fechar_janela()).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(janela_confirmacao, text='Confirmar', command=lambda: Excluir_Nivel()).grid(row=1, column=1, padx=5, pady=5)

    Centralizar_Janela(janela_confirmacao)
    janela_confirmacao.mainloop()