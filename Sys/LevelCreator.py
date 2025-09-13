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
        Matriz_Estrutural = []
        num_linhas = None
        num_colunas = None
        janela.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela.title("Criar nível")
    janela.resizable(False, False)

    largura_janela, altura_janela = Calcular_Tamanho_Janela(num_linhas, num_colunas)
    janela.geometry(f'{largura_janela}x{altura_janela}')

    # CONFIGURAÇÃO CORRIGIDA - Configure a JANELA, não a raiz
    janela.grid_rowconfigure(0, weight=1)  # 3 partes para a matriz
    janela.grid_rowconfigure(1, weight=1)  # 1 parte para as peças
    janela.grid_columnconfigure(0, weight=1)

    Centralizar_Janela(janela)
    # Frame principal para a matriz
    frame_nivel = tk.Frame(janela,)
    frame_nivel.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    
    # Configure o frame_nivel para expandir
    frame_nivel.grid_rowconfigure(0, weight=1)
    frame_nivel.grid_columnconfigure(0, weight=1)  # esquerda
    frame_nivel.grid_columnconfigure(1, weight=1)  # matriz (maior peso)
    frame_nivel.grid_columnconfigure(2, weight=1)  # direita

    frame_esquerda = tk.Frame(frame_nivel, width=80)
    frame_direita = tk.Frame(frame_nivel, width=80)
    frame_matriz_estrutural = tk.Frame(frame_nivel)
    
    frame_esquerda.grid(row=0, column=0, sticky='ns')
    frame_matriz_estrutural.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    frame_direita.grid(row=0, column=2, sticky='ns')

    # Configure a matriz para expandir
    for i in range(num_linhas):
        frame_matriz_estrutural.grid_rowconfigure(i, weight=1, uniform="peca_row")
    for j in range(num_colunas):
        frame_matriz_estrutural.grid_columnconfigure(j, weight=1, uniform="peca_col")

    tk.Label(frame_esquerda, text="Início", font=("Arial", 14), fg='green').pack(side='bottom', pady=10)

    def Salvar_Nivel():
        global Matriz_Estrutural
        nivel_valido = LRunner.Rotina_Verifica_Nivel_Valido(Matriz_Estrutural)

        if nivel_valido: Exibir_Janela_Salvar_Nivel(raiz)

    tk.Button(frame_esquerda, text="Salvar nível", font=("Arial", 14), bg='green', fg='white',
                            command=lambda: Salvar_Nivel()).pack(side='top', pady=10)

    tk.Label(frame_direita, text="Fim", font=("Arial", 14), fg='red').pack(side='top', pady=10)

    janela.botoes_pecas = {}
    janela.imagens_pecas = []
    
    # Cria botões
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):
            botao = tk.Button(frame_matriz_estrutural, state='normal', 
                            command=lambda l=indice_linha, c=indice_coluna: Clique_Botao_Matriz_Estrutural(janela, l, c))
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            janela.botoes_pecas[(indice_linha, indice_coluna)] = botao

    def atualizar_imagens():
        if janela.botoes_pecas:
            frame_matriz_estrutural.update_idletasks()
            
            largura_frame = frame_matriz_estrutural.winfo_width()
            altura_frame = frame_matriz_estrutural.winfo_height()
            
            largura_botao = largura_frame // num_colunas
            altura_botao = altura_frame // num_linhas

            tamanho_imagem = min(largura_botao, altura_botao) - 2
            
            for (linha, coluna), botao in janela.botoes_pecas.items():
                peca_id = Matriz_Estrutural[linha][coluna]
                imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
                janela.imagens_pecas.append(imagem_peca)
                botao.config(image=imagem_peca)
                botao.image = imagem_peca
    
    # Chama após um breve delay para garantir que a janela esteja renderizada
    janela.after(100, atualizar_imagens)

    Gera_Secao_Todas_As_Pecas(janela)

def Clique_Botao_Matriz_Estrutural(raiz, linha, coluna):
    global Botao_Selecionado

    if (Botao_Selecionado == raiz.botoes_pecas[(linha, coluna)]):
        Botao_Selecionado.config(bg='SystemButtonFace')
        Botao_Selecionado = None
        return

    if (Botao_Selecionado is not None): 
        Botao_Selecionado.config(bg='SystemButtonFace')

    Botao_Selecionado = raiz.botoes_pecas[(linha, coluna)]
    Botao_Selecionado.config(bg='red')#, state='readonly')
    Botao_Selecionado.linha = linha
    Botao_Selecionado.coluna = coluna

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

def Gera_Secao_Todas_As_Pecas(janela):
    frame_pecas = tk.Frame(janela)
    frame_pecas.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)
    
    # Configure o frame de peças para ter a mesma estrutura
    num_linhas_pecas = 2
    num_colunas_pecas = 8
    
    for i in range(num_linhas_pecas):
        frame_pecas.grid_rowconfigure(i, weight=1)
    for j in range(num_colunas_pecas):
        frame_pecas.grid_columnconfigure(j, weight=1)

    pecas = crud.Buscar_Pecas()
    janela.matriz_pecas = []
    
    indice_peca_atual = 0
    for linha in range(num_linhas_pecas):
        linha = []
        for coluna in range(num_colunas_pecas):
            linha.append( pecas[indice_peca_atual]['id'] )
            if indice_peca_atual < len(pecas) + 1 : indice_peca_atual += 1
        janela.matriz_pecas.append(linha)
    
    janela.botoes_pecas_padrao = {}
    
    # Cria botões padrões com a mesma configuração
    for indice_linha in range(num_linhas_pecas):
        for indice_coluna in range(num_colunas_pecas):
            botao = tk.Button(frame_pecas, state='normal', 
                            command=lambda l=indice_linha, c=indice_coluna: Clique_Botao_Matriz_Pecas(janela, l, c))
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            janela.botoes_pecas_padrao[(indice_linha, indice_coluna)] = botao

    def atualizar_imagens_pecas():
        # Usa o mesmo tamanho das imagens principais
        frame_pecas.update_idletasks()
        largura_frame = frame_pecas.winfo_width()
        altura_frame = frame_pecas.winfo_height()
        largura_botao = largura_frame // num_colunas_pecas
        altura_botao = altura_frame // num_linhas_pecas
        tamanho_imagem = min(largura_botao, altura_botao) - 2
        
        for (linha, coluna), botao in janela.botoes_pecas_padrao.items():
            peca_id = janela.matriz_pecas[linha][coluna]
            imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
            janela.imagens_pecas.append(imagem_peca)
            botao.config(image=imagem_peca)
            botao.image = imagem_peca
    
    # Espera um pouco mais para garantir que o tamanho principal esteja disponível
    janela.after(300, atualizar_imagens_pecas)

def Clique_Botao_Matriz_Pecas(raiz, linha, coluna):
    global Matriz_Estrutural, Botao_Selecionado
    if Botao_Selecionado is None: return

    nivel_id = raiz.matriz_pecas[linha][coluna]
    Matriz_Estrutural[Botao_Selecionado.linha][Botao_Selecionado.coluna] = nivel_id

    Botao_Selecionado.update_idletasks()

    tamanho_img_atual = min(Botao_Selecionado.winfo_height(), Botao_Selecionado.winfo_width()) - 2
    nova_imagem = LRunner.Buscar_Imagem_Peca(nivel_id, (tamanho_img_atual, tamanho_img_atual))
    raiz.imagens_pecas.append(nova_imagem)

    Botao_Selecionado.config(bg='SystemButtonFace', image=nova_imagem)
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
    janela_confirmacao.geometry('300x200')

    tk.Label(janela_confirmacao, text="Nome do nível:").grid(row=0, column=0, sticky='w', pady=(0, 5))
    nome_nivel = tk.Entry(janela_confirmacao, width=20)
    nome_nivel.grid(row=0, column=1, pady=(0, 5))
    nome_nivel.focus()

    def Persistir_Nivel():
        nome_nivel_string = nome_nivel.get()
        crud.Salvar_Nivel(nome_nivel_string, 'facil', Matriz_Estrutural,  Obter_Usuario_Atual())
        ao_fechar_janela()

    tk.Button(janela_confirmacao, text='Cancelar', command=lambda: ao_fechar_janela()).grid(row=1, column=0)
    tk.Button(janela_confirmacao, text='Salvar', command=lambda: Persistir_Nivel()).grid(row=1, column=1)

    Centralizar_Janela(janela_confirmacao)
    janela_confirmacao.mainloop()