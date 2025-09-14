import tkinter as tk
from tkinter import messagebox
from Sys.Login import Centralizar_Janela, Obter_Usuario_Atual
import Sys.LevelRunner as LRunner
import Sys.Crud as crud
import Sys.LevelRunner as LRunner

num_linhas = None
num_colunas = None
Matriz_Estrutural = []
Botao_Selecionado = None

def Gerar_Pagina_Criacao_Nivel(raiz):
    Exibir_Janela_Dimensoes_Nivel(raiz)

def Exibir_Janela_Dimensoes_Nivel(raiz):
    janela = tk.Toplevel(raiz)
    janela.transient(raiz)
    janela.grab_set()
    janela.focus_force()

    def ao_fechar_janela():
        janela.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela.title("Criar nível")
    janela.resizable(False, False)

    frame_entradas = tk.Frame(janela)
    frame_entradas.pack(expand=True, fill='both', padx=10, pady=10)

    tk.Label(frame_entradas, text="Número de linhas:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
    entrada_linhas = tk.Entry(frame_entradas, width=20)
    entrada_linhas.grid(row=0, column=1, padx=5, pady=5)
    entrada_linhas.focus()

    tk.Label(frame_entradas, text="Número de colunas:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
    entrada_colunas = tk.Entry(frame_entradas, width=20)
    entrada_colunas.grid(row=1, column=1, padx=5, pady=5)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(expand=True, fill='both', padx=10, pady=10)

    def Salvar_Dimensoes():
        linhas = entrada_linhas.get()
        colunas = entrada_colunas.get()

        if not linhas or not colunas:
            messagebox.showerror("Erro!", "Você deve informar a quantidade de linhas e de colunas para a geração do nível.")
            return
        elif (not linhas.isnumeric()) or (not colunas.isnumeric()):
            messagebox.showerror("Erro!", "Quantidade de linhas e colunas deve ser inteira.")
            return
        elif (int(linhas) <= 0) or (int(colunas) <= 0):
            messagebox.showerror("Erro!", "Você deve informar uma quantidade de linhas e de colunas maior que zero.")
            return
        elif (int(linhas) > 8) or (int(colunas) > 8):
            messagebox.showerror("Erro!", "Número máximo de linhas e colnas é 8.")
            return

        global num_linhas, num_colunas
        num_linhas = int(linhas)
        num_colunas = int(colunas)
        Definir_Matriz_Estrutural()
        ao_fechar_janela()
        Exibir_Janela_Criacao_Nivel(raiz)

    tk.Button(frame_botoes, text='Criar nível', command= lambda: Salvar_Dimensoes(), width=10).pack(side='right', padx=5)
    tk.Button(frame_botoes, text='Cancelar', command= lambda: ao_fechar_janela(), width=10).pack(side='right', padx=5)
    entrada_colunas.bind('<Return>', lambda e: Salvar_Dimensoes())

    Centralizar_Janela(janela)

def Definir_Matriz_Estrutural():
    global num_linhas, num_colunas, Matriz_Estrutural

    for indice_linha in range(num_linhas):
        linha = []
        for indice_coluna in range(num_colunas):
            linha.append(0)
        Matriz_Estrutural.append(linha)

def Exibir_Janela_Criacao_Nivel(raiz):
    global num_linhas, num_colunas, Matriz_Estrutural

    janela = tk.Toplevel(raiz)
    janela.transient(raiz)
    janela.grab_set()
    janela.focus_force()

    def ao_fechar_janela():
        global num_linhas, num_colunas, Matriz_Estrutural

        Matriz_Estrutural = []
        num_linhas = None
        num_colunas = None
        janela.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela.title("Criar nível")
    janela.resizable(True, True)

    tamanho_botao = Calcular_Tamanho_Botao(num_linhas, num_colunas)
    
    largura_frame_nivel = (num_colunas * tamanho_botao) + (2 * num_colunas * 1) + (2 * 5) #TAMANHO BOTOES + MARGEM 1PX BOTOES + MARGEM FRAMES
    altura_frame_nivel = (num_linhas * tamanho_botao) + (2 * num_linhas * 1) + (2 * 5) #TAMANHO BOTOES + MARGEM 1PX + MARGEM FRAMES
    
    largura_frame_pecas = (8 * tamanho_botao) + (2 * 8) + (2 * 10)
    altura_frame_pecas = (2 * tamanho_botao) + (2 * 2) + (2 * 10)

    largura_janela = max(largura_frame_nivel, largura_frame_pecas) + 200  
    altura_janela = altura_frame_nivel + altura_frame_pecas + 100  

    janela.geometry(f'{largura_janela}x{altura_janela}')

    janela.grid_rowconfigure(0, weight=0) 
    janela.grid_rowconfigure(1, weight=0)  
    janela.grid_columnconfigure(0, weight=0)

    Centralizar_Janela(janela)

    frame_nivel = tk.Frame(janela)
    frame_nivel.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    
    frame_nivel.grid_rowconfigure(0, weight=1)
    frame_nivel.grid_columnconfigure(0, weight=1)
    frame_nivel.grid_columnconfigure(1, weight=0)
    frame_nivel.grid_columnconfigure(2, weight=1)

    frame_esquerda = tk.Frame(frame_nivel, width=80)
    frame_direita = tk.Frame(frame_nivel, width=80)
    frame_matriz_estrutural = tk.Frame(frame_nivel)
    
    frame_matriz_estrutural.grid_propagate(True)
    
    frame_esquerda.grid(row=0, column=0, sticky='nse')
    frame_matriz_estrutural.grid(row=0, column=1, sticky='', padx=5, pady=5)
    frame_direita.grid(row=0, column=2, sticky='nsw')

    for i in range(num_linhas):
        frame_matriz_estrutural.grid_rowconfigure(i, weight=0, minsize=tamanho_botao)
    for j in range(num_colunas):
        frame_matriz_estrutural.grid_columnconfigure(j, weight=0, minsize=tamanho_botao)

    tk.Label(frame_esquerda, text="Início", font=("Arial", 14), fg='green').pack(side='bottom', pady=10)

    def Salvar_Nivel():
        global Matriz_Estrutural
        nivel_valido = LRunner.Rotina_Verifica_Nivel_Valido(Matriz_Estrutural)

        if nivel_valido: 
            Exibir_Janela_Salvar_Nivel(raiz)
        else:
            messagebox.showerror("Opss", "O nível criado não é válido!")

    tk.Button(frame_esquerda, text="Salvar nível", font=("Arial", 14), bg='green', fg='white',
                            command=lambda: Salvar_Nivel()).pack(side='top', pady=10)

    tk.Label(frame_direita, text="Fim", font=("Arial", 14), fg='red').pack(side='top', pady=10, anchor='w')

    janela.botoes_pecas = {}
    janela.imagens_pecas = []
    
    tamanho_imagem = tamanho_botao - 2
    
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):

            imagem_inicial = LRunner.Buscar_Imagem_Peca(0, (tamanho_imagem, tamanho_imagem))
            janela.imagens_pecas.append(imagem_inicial)
            
            botao = tk.Button(frame_matriz_estrutural, 
                             image=imagem_inicial,
                             state='normal',
                             width=tamanho_botao,
                             height=tamanho_botao,
                             command=lambda l=indice_linha, c=indice_coluna: Clique_Botao_Matriz_Estrutural(janela, l, c))
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            janela.botoes_pecas[(indice_linha, indice_coluna)] = botao

    Gera_Secao_Todas_As_Pecas(janela, tamanho_botao)


def Clique_Botao_Matriz_Estrutural(raiz, linha, coluna):
    global Botao_Selecionado

    if (Botao_Selecionado == raiz.botoes_pecas[(linha, coluna)]):
        Botao_Selecionado.config(bg='SystemButtonFace')
        Botao_Selecionado = None
        return

    if (Botao_Selecionado is not None): 
        Botao_Selecionado.config(bg='SystemButtonFace')

    Botao_Selecionado = raiz.botoes_pecas[(linha, coluna)]
    Botao_Selecionado.config(bg='red')
    Botao_Selecionado.linha = linha
    Botao_Selecionado.coluna = coluna

def Calcular_Tamanho_Botao(num_linhas, num_colunas):
    """Calcula o tamanho fixo dos botões baseado no tamanho da matriz"""
    if num_linhas <= 3 and num_colunas <= 3:
        return 120 
    elif num_linhas <= 5 and num_colunas <= 5:
        return 90   
    else:
        return 70  


def Gera_Secao_Todas_As_Pecas(janela, tamanho_botao):
    frame_pecas = tk.Frame(janela)
    frame_pecas.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    
    num_linhas_pecas = 2
    num_colunas_pecas = 8
    
    for i in range(num_linhas_pecas):
        frame_pecas.grid_rowconfigure(i, weight=0, minsize=tamanho_botao)
    for j in range(num_colunas_pecas):
        frame_pecas.grid_columnconfigure(j, weight=0, minsize=tamanho_botao)

    pecas = crud.Buscar_Pecas()
    janela.matriz_pecas = []
    
    indice_peca_atual = 0
    for linha in range(num_linhas_pecas):
        linha_pecas = []
        for coluna in range(num_colunas_pecas):
            if indice_peca_atual < len(pecas):
                linha_pecas.append(pecas[indice_peca_atual]['id'])
                indice_peca_atual += 1
            else:
                linha_pecas.append(0) 
        janela.matriz_pecas.append(linha_pecas)
    
    janela.botoes_pecas_padrao = {}
    
    tamanho_imagem = tamanho_botao - 2
    
    for indice_linha in range(num_linhas_pecas):
        for indice_coluna in range(num_colunas_pecas):
            peca_id = janela.matriz_pecas[indice_linha][indice_coluna]
            imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
            janela.imagens_pecas.append(imagem_peca)
            
            botao = tk.Button(frame_pecas, 
                             image=imagem_peca,
                             state='normal',
                             width=tamanho_botao,
                             height=tamanho_botao,
                             command=lambda l=indice_linha, c=indice_coluna: Clique_Botao_Matriz_Pecas(janela, l, c))
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            janela.botoes_pecas_padrao[(indice_linha, indice_coluna)] = botao

def Clique_Botao_Matriz_Pecas(raiz, linha, coluna):
    global Matriz_Estrutural, Botao_Selecionado
    if Botao_Selecionado is None: 
        return

    peca_id = raiz.matriz_pecas[linha][coluna]
    Matriz_Estrutural[Botao_Selecionado.linha][Botao_Selecionado.coluna] = peca_id

    tamanho_botao = Botao_Selecionado.winfo_width()
    tamanho_imagem = tamanho_botao - 2 
    nova_imagem = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
    raiz.imagens_pecas.append(nova_imagem)

    Botao_Selecionado.config(bg='SystemButtonFace', image=nova_imagem)
    Botao_Selecionado.image = nova_imagem
    Botao_Selecionado = None

def Exibir_Janela_Salvar_Nivel(raiz):
    janela_confirmacao = tk.Toplevel(raiz)
    janela_confirmacao.transient(raiz)
    janela_confirmacao.grab_set()
    janela_confirmacao.focus_force()

    def ao_fechar_janela():
        janela_confirmacao.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela_confirmacao.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela_confirmacao.title("Salvar nível")
    janela_confirmacao.resizable(False, False)

    tk.Label(janela_confirmacao, text="Nome do nível:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
    nome_nivel = tk.Entry(janela_confirmacao, width=20)
    nome_nivel.grid(row=0, column=1, padx=5, pady=5)
    nome_nivel.focus()

    def Persistir_Nivel():
        nome_nivel_string = nome_nivel.get()
        crud.Salvar_Nivel(nome_nivel_string, 'facil', Matriz_Estrutural,  Obter_Usuario_Atual())
        messagebox.showinfo("Operação concluída", "Nível salvo com sucesso!")
        ao_fechar_janela()

    tk.Button(janela_confirmacao, text='Cancelar', command=lambda: ao_fechar_janela()).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(janela_confirmacao, text='Salvar', command=lambda: Persistir_Nivel()).grid(row=1, column=1, padx=5, pady=5)

    Centralizar_Janela(janela_confirmacao)
    janela_confirmacao.mainloop()