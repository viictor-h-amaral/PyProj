"""
Módulo de criação de níveis.

Responsável pela interface e lógica para criação de novos níveis do jogo,
incluindo definição de dimensões, posicionamento de peças e salvamento.
"""

import tkinter as tk
from tkinter import messagebox
from Sys.Login import Centralizar_Janela, Obter_Usuario_Atual
import Sys.LevelRunner as LRunner
import Sys.Crud as crud
import Sys.WindowsPattern as pattern

# Variáveis globais para estado da criação
num_linhas = None
num_colunas = None
Matriz_Estrutural = []
Botao_Selecionado = None


def Limpar_Variaveis_Globais():
    """Limpa todas as variáveis globais do módulo."""
    global num_linhas, num_colunas, Matriz_Estrutural, Botao_Selecionado
    num_linhas = None
    num_colunas = None
    Matriz_Estrutural = []
    Botao_Selecionado = None


def Gerar_Pagina_Criacao_Nivel(raiz):
    """Inicia o processo de criação de nível exibindo a janela de dimensões."""
    Exibir_Janela_Dimensoes_Nivel(raiz)


def Exibir_Janela_Dimensoes_Nivel(raiz):
    """
    Exibe janela para definição das dimensões do nível.
    
    Args:
        raiz: Janela pai para a janela modal
    """
    janela = tk.Toplevel(raiz)
    janela.transient(raiz)
    janela.grab_set()
    janela.focus_force()

    def ao_fechar_janela():
        """Callback para fechar a janela e retornar o foco."""
        janela.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela.title("Criar nível")
    janela.resizable(False, False)

    frame_entradas = tk.Frame(janela)
    frame_entradas.pack(expand=True, fill='both', padx=10, pady=10)

    tk.Label(frame_entradas, 
                text="Número de linhas:", 
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao
            ).grid(row=0, column=0, sticky='w', padx=5, pady=5)

    entrada_linhas = tk.Entry(frame_entradas, 
                                width=20, 
                                font=pattern.fonte_texto,
                                fg=pattern.cor_fonte_padrao)
    entrada_linhas.grid(row=0, column=1, padx=5, pady=5)
    entrada_linhas.focus()

    tk.Label(frame_entradas, 
                text="Número de colunas:", 
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao
            ).grid(row=1, column=0, sticky='w', padx=5, pady=5)

    entrada_colunas = tk.Entry(frame_entradas, 
                                width=20, 
                                font=pattern.fonte_texto,
                                fg=pattern.cor_fonte_padrao)
    entrada_colunas.grid(row=1, column=1, padx=5, pady=5)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(expand=True, fill='both', padx=10, pady=10)

    def Salvar_Dimensoes():
        """Valida e salva as dimensões informadas pelo usuário."""
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

    tk.Button(frame_botoes, 
                text='Criar nível', 
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao,
                bg=pattern.cor_fria_paleta,
                command=lambda: Salvar_Dimensoes(), 
                width=15
            ).pack(side='right', padx=5)

    tk.Button(frame_botoes, 
                text='Cancelar', 
                font=pattern.fonte_cabecalho_12, 
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                command=lambda: ao_fechar_janela(), 
                width=15
            ).pack(side='right', padx=5)

    entrada_colunas.bind('<Return>', lambda e: Salvar_Dimensoes())

    Centralizar_Janela(janela)


def Definir_Matriz_Estrutural():
    """Inicializa a matriz estrutural com peças inicial e final padrão."""
    global num_linhas, num_colunas, Matriz_Estrutural

    for indice_linha in range(num_linhas):
        linha = []
        for indice_coluna in range(num_colunas):
            linha.append(0)
        Matriz_Estrutural.append(linha)

    coordenada_peca_inicial = LRunner.Coordenada_Peca_Inicial(Matriz_Estrutural)
    Matriz_Estrutural[coordenada_peca_inicial[0]][coordenada_peca_inicial[1]] = 12

    coordenada_peca_final = LRunner.Coordenada_Peca_Final(Matriz_Estrutural)
    Matriz_Estrutural[coordenada_peca_final[0]][coordenada_peca_final[1]] = 14


def Exibir_Janela_Criacao_Nivel(raiz):
    """
    Exibe a janela principal de criação de nível com a matriz de peças.
    
    Args:
        raiz: Janela pai para a janela de criação
    """
    global num_linhas, num_colunas, Matriz_Estrutural

    janela = tk.Toplevel(raiz)
    janela.transient(raiz)
    janela.grab_set()
    janela.focus_force()

    def ao_fechar_janela():
        """Callback para fechar a janela e limpar variáveis."""
        Limpar_Variaveis_Globais()
        janela.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela.title("Criar nível")
    janela.resizable(True, True)

    tamanho_botao = Calcular_Tamanho_Botao(num_linhas, num_colunas)
    
    largura_frame_nivel = (num_colunas * tamanho_botao) + (2 * num_colunas * 1) + (2 * 5)
    altura_frame_nivel = (num_linhas * tamanho_botao) + (2 * num_linhas * 1) + (2 * 5)
    
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

    tk.Label(frame_esquerda, 
                text="Início", 
                font=pattern.fonte_cabecalho_22, 
                fg=pattern.cor_fria_paleta
            ).pack(side='bottom', pady=10)

    def Salvar_Nivel():
        """Valida e persiste o nível criado."""
        global Matriz_Estrutural
        nivel_valido = LRunner.Rotina_Verifica_Nivel_Valido(Matriz_Estrutural)

        if nivel_valido: 
            Exibir_Janela_Salvar_Nivel(janela)
        else:
            messagebox.showerror("Opss", "O nível criado não é válido!")

    tk.Button(frame_esquerda, 
                text="Salvar nível", 
                font=pattern.fonte_cabecalho_12, 
                fg=pattern.cor_fonte_padrao,
                bg=pattern.verde, 
                command=lambda: Salvar_Nivel()
            ).pack(side='top', pady=10)

    tk.Label(frame_direita, 
                text="Fim", 
                font=pattern.fonte_cabecalho_22, 
                fg=pattern.cor_quente_paleta
            ).pack(side='top', pady=10, anchor='w')

    janela.botoes_pecas = {}
    janela.imagens_pecas = []
    
    tamanho_imagem = tamanho_botao - 2
    
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):
            peca_id = Matriz_Estrutural[indice_linha][indice_coluna]
            imagem_inicial = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
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
    """
    Manipula o clique em um botão da matriz estrutural.
    
    Args:
        raiz: Janela principal
        linha: Linha do botão clicado
        coluna: Coluna do botão clicado
    """
    global Botao_Selecionado

    if (Botao_Selecionado == raiz.botoes_pecas[(linha, coluna)]):
        Botao_Selecionado.config(bg='SystemButtonFace')
        Botao_Selecionado = None
        return

    if (Botao_Selecionado is not None): 
        Botao_Selecionado.config(bg='SystemButtonFace')

    Botao_Selecionado = raiz.botoes_pecas[(linha, coluna)]
    Botao_Selecionado.config(bg=pattern.cor_quente_paleta)
    Botao_Selecionado.linha = linha
    Botao_Selecionado.coluna = coluna


def Calcular_Tamanho_Botao(num_linhas, num_colunas):
    """
    Calcula o tamanho fixo dos botões baseado no tamanho da matriz.
    
    Args:
        num_linhas: Número de linhas da matriz
        num_colunas: Número de colunas da matriz
        
    Returns:
        int: Tamanho do botão em pixels
    """
    if num_linhas <= 3 and num_colunas <= 3:
        return 120 
    elif num_linhas <= 5 and num_colunas <= 5:
        return 90   
    else:
        return 70  


def Gera_Secao_Todas_As_Pecas(janela, tamanho_botao):
    """
    Gera a seção com todas as peças disponíveis para seleção.
    
    Args:
        janela: Janela principal
        tamanho_botao: Tamanho dos botões das peças
    """
    frame_pecas = tk.Frame(janela)
    frame_pecas.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    
    num_linhas_pecas = 2
    num_colunas_pecas = 8
    
    for i in range(num_linhas_pecas):
        frame_pecas.grid_rowconfigure(i, weight=0, minsize=tamanho_botao)
    for j in range(num_colunas_pecas):
        frame_pecas.grid_columnconfigure(j, weight=0, minsize=tamanho_botao)

    janela.matriz_pecas = []
    
    janela.matriz_pecas =   [[0, 41, 11, 12, 13, 14, 21, 22], 
                             [23, 24, 25, 26, 31, 32, 33, 34]]

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
    """
    Manipula o clique em uma peça da matriz de peças disponíveis.
    
    Args:
        raiz: Janela principal
        linha: Linha da peça clicada
        coluna: Coluna da peça clicada
    """
    global Matriz_Estrutural, Botao_Selecionado
    if Botao_Selecionado is None: 
        return

    endereco_botao_selecionado = (Botao_Selecionado.linha, Botao_Selecionado.coluna)
    coordenadas_pecas_final_inicial = [LRunner.Coordenada_Peca_Final(Matriz_Estrutural) , LRunner.Coordenada_Peca_Inicial(Matriz_Estrutural)]
    nova_peca_id = raiz.matriz_pecas[linha][coluna]

    if ((endereco_botao_selecionado in coordenadas_pecas_final_inicial) 
        and nova_peca_id not in crud.Buscar_Grupo_Pecas_Por_Id(2)['pecas']):
        messagebox.showwarning("Aviso!", "As peças inicial e final devem conter somente peças com uma única saída/entrada.")
        return

    Matriz_Estrutural[Botao_Selecionado.linha][Botao_Selecionado.coluna] = nova_peca_id

    tamanho_botao = Botao_Selecionado.winfo_width()
    tamanho_imagem = tamanho_botao - 2 
    nova_imagem = LRunner.Buscar_Imagem_Peca(nova_peca_id, (tamanho_imagem, tamanho_imagem))
    raiz.imagens_pecas.append(nova_imagem)

    Botao_Selecionado.config(bg='SystemButtonFace', image=nova_imagem)
    Botao_Selecionado.image = nova_imagem
    Botao_Selecionado = None


def Exibir_Janela_Salvar_Nivel(raiz):
    """
    Exibe janela para salvar o nível criado com nome e dificuldade.
    
    Args:
        raiz: Janela pai para a janela modal
    """
    janela_confirmacao = tk.Toplevel(raiz)
    janela_confirmacao.transient(raiz)
    janela_confirmacao.grab_set()
    janela_confirmacao.focus_force()

    def ao_fechar_janela():
        """Callback para fechar a janela de confirmação."""
        janela_confirmacao.destroy()
        raiz.focus_force()
        raiz.grab_set()
    
    janela_confirmacao.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    janela_confirmacao.title("Salvar nível")
    janela_confirmacao.resizable(False, False)

    frame_nome_nivel = tk.Frame(janela_confirmacao)
    frame_nome_nivel.grid(row=0, column=0, sticky='w', padx=5, pady=5)

    tk.Label(frame_nome_nivel, 
                text="Nome do nível:", 
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao
            ).grid(row=0, column=0, sticky='w', padx=5, pady=5)

    nome_nivel = tk.Entry(frame_nome_nivel, 
                            width=20, 
                            font=pattern.fonte_texto,
                            fg=pattern.cor_fonte_padrao)
    nome_nivel.grid(row=0, column=1, padx=5, pady=5)
    nome_nivel.focus()

    frame_nivel_dificuldade = tk.Frame(janela_confirmacao)
    frame_nivel_dificuldade.grid(row=1, column=0, sticky='w', padx=5, pady=5)

    tk.Label(frame_nivel_dificuldade, 
                text="Nível de dificuldade:", 
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao
            ).grid(row=0, column=0, columnspan=3, sticky='w', padx=5, pady=5)

    dificuldade_novo_nivel = tk.StringVar(value="facil")
    radio_facil = tk.Radiobutton(frame_nivel_dificuldade, 
                                    text="Fácil", 
                                    font=pattern.fonte_texto, 
                                    fg=pattern.cor_fonte_padrao,
                                    variable=dificuldade_novo_nivel, 
                                    value="facil")
    radio_facil.grid(row=1, column=0, sticky='w')

    radio_medio = tk.Radiobutton(frame_nivel_dificuldade, 
                                text="Médio", 
                                font=pattern.fonte_texto, 
                                fg=pattern.cor_fonte_padrao,
                                variable=dificuldade_novo_nivel, 
                                value="medio")
    radio_medio.grid(row=1, column=1, sticky='w')

    radio_dificil = tk.Radiobutton(frame_nivel_dificuldade, 
                                    text="Difícil", 
                                    font=pattern.fonte_texto, 
                                    fg=pattern.cor_fonte_padrao, 
                                    variable=dificuldade_novo_nivel, 
                                    value="dificil")
    radio_dificil.grid(row=1, column=2, sticky='w')

    frame_botoes = tk.Frame(janela_confirmacao)
    frame_botoes.grid(row=2, column=0, padx=5, pady=5)

    def Persistir_Nivel():
        """Persiste o nível no banco de dados."""
        global Matriz_Estrutural
        nome_nivel_string = nome_nivel.get()
        dificuldade = dificuldade_novo_nivel.get()

        if not nome_nivel_string or not dificuldade:
            messagebox.showerror("Opss", "Você deve informar o nome e a dificuldade do nível para prosseguir!")
            return
        elif len(nome_nivel_string) > 100:
            messagebox.showerror("Opss", "Máximo de caracteres para o nome do nível é 100!")
            return

        crud.Salvar_Nivel(nome_nivel_string, dificuldade, Matriz_Estrutural,  Obter_Usuario_Atual())
        messagebox.showinfo("Operação concluída", "Nível salvo com sucesso!")
        ao_fechar_janela()
        raiz.destroy()
        Limpar_Variaveis_Globais()

    tk.Button(frame_botoes, 
                text='Cancelar', 
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                width=15,
                command=lambda: ao_fechar_janela()
            ).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(frame_botoes, 
                text='Salvar', 
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao, 
                bg=pattern.cor_fria_paleta, 
                width=15,
                command=lambda: Persistir_Nivel()
            ).grid(row=0, column=1, padx=5, pady=5)

    Centralizar_Janela(janela_confirmacao)
    janela_confirmacao.mainloop()