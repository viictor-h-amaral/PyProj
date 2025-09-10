import tkinter as tk
from tkinter import messagebox
from Sys.Login import Centralizar_Janela
import Sys.LevelRunner as LRunner

num_linhas = None
num_colunas = None
Matriz_Estrutural = []

def Gerar_Pagina_Criacao_Nivel(raiz):
    Exibir_Janela_Dimensoes_Nivel(raiz)
    #Exibir_Janela_Criacao_Nivel(raiz)

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
    janela.geometry("300x200")
    janela.resizable(False, False)

    frame_entradas = tk.Frame(janela)
    frame_entradas.pack(expand=True, fill='both', padx=10, pady=10)

    tk.Label(frame_entradas, text="Número de linhas:").grid(row=0, column=0, sticky='w', pady=(0, 5))
    entrada_linhas = tk.Entry(frame_entradas, width=20)
    entrada_linhas.grid(row=0, column=1, pady=(0, 5))
    entrada_linhas.focus()

    tk.Label(frame_entradas, text="Número de colunas:").grid(row=1, column=0, sticky='w', pady=(0, 5))
    entrada_colunas = tk.Entry(frame_entradas, width=20)
    entrada_colunas.grid(row=1, column=1, pady=(0, 5))
    entrada_colunas.focus()

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

        global num_linhas, num_colunas
        num_linhas = int(linhas)
        num_colunas = int(colunas)
        Definir_Matriz_Estrutural()
        ao_fechar_janela()
        Exibir_Janela_Criacao_Nivel(raiz)

    tk.Button(frame_botoes, text='Criar nível', command= lambda: Salvar_Dimensoes(), width=10).pack(side='right', padx=5)
    tk.Button(frame_botoes, text='Cancelar', command= lambda: ao_fechar_janela(), width=10).pack(side='right', padx=5)

    Centralizar_Janela(janela)
    janela.mainloop()

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
        janela.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela.title("Criar nível")
    largura_janela, altura_janela = Calcular_Tamanho_Janela(num_linhas, num_colunas)
    janela.geometry(f'{largura_janela}x{altura_janela}')
    janela.resizable(False, False)
    
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(1, weight=1)
    
    frame_esquerda = tk.Frame(janela, width=100)
    frame_direita = tk.Frame(janela, width=100)
    frame_nivel = tk.Frame(janela)
    
    frame_esquerda.grid(row=0, column=0, sticky='ns')
    frame_nivel.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
    frame_direita.grid(row=0, column=2, sticky='ns')
    
    for i in range(num_linhas):
        frame_nivel.grid_rowconfigure(i, weight=1, uniform="peca_row")
    for j in range(num_colunas):
        frame_nivel.grid_columnconfigure(j, weight=1, uniform="peca_col")

    tk.Label(frame_esquerda, text="Início", font=("Arial", 14), fg='green').pack(side='bottom', pady=10)
    tk.Label(frame_direita, text="Fim", font=("Arial", 14), fg='red').pack(side='top', pady=10)

    janela.botoes_pecas = {}
    janela.imagens_pecas = []
    
    # Cria botões desabilitados primeiro
    botoes = {}
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):
            botao = tk.Button(frame_nivel, state='normal', command= lambda l=indice_linha, c=indice_coluna: Clique_Botao(janela, l, c))
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            botoes[(indice_linha, indice_coluna)] = botao

    def atualizar_imagens():
        if botoes:
            primeiro_botao = list(botoes.values())[0]
            primeiro_botao.update_idletasks()
            largura_botao = primeiro_botao.winfo_width()
            altura_botao = primeiro_botao.winfo_height()
            
            tamanho_imagem = min(largura_botao, altura_botao) - 2
            
            for (linha, coluna), botao in botoes.items():
                peca_id = Matriz_Estrutural[linha][coluna]
                imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
                janela.imagens_pecas.append(imagem_peca)
                botao.config(image=imagem_peca)
                botao.image = imagem_peca
    
    janela.after(100, atualizar_imagens)

    janela.mainloop()

def Clique_Botao(raiz, linha, coluna):
    return

def Calcular_Tamanho_Janela(num_linhas, num_colunas):
    """
    Calcula o tamanho ideal da janela baseado na matriz
    Mantém peças maiores para matrizes pequenas e ajusta para matrizes grandes
    """
    
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
    
    return largura_total, altura_total