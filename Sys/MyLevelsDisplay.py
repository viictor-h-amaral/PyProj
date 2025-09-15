from pathlib import Path
import Sys.Crud as crud
import Sys.LevelRunner as LRunner
import tkinter as tk
from Sys.Login import Obter_Usuario_Atual, Centralizar_Janela
from tkinter import messagebox
import Sys.Codifier as codifier
import Sys.WindowsPattern as pattern

# Variáveis globais para armazenamento do estado atual
Nivel = None
Estrutura = None
Matriz_Estrutural = None

# Controle de paginação para exibição de níveis [início, fim]
controle_meus_niveis_exibidos = [0, 10]
Usuario_Atual = None

def Exibir_Meu_Nivel(nivel_id, pagina, frame_sup, frame_inf):
    """
    Exibe um nível específico em uma janela modal com visualização detalhada.
    
    Parameters:
        nivel_id (int): ID do nível a ser exibido
        pagina (tk.Toplevel): Janela pai da qual esta janela depende
        frame_sup (tk.Frame): Frame superior para atualização após exclusão
        frame_inf (tk.Frame): Frame inferior para atualização após exclusão
    
    Global:
        Atualiza as variáveis globais Nivel, Estrutura e Matriz_Estrutural
    
    Returns:
        None
    """
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
        """Fecha a janela do nível e retorna o foco para a página pai."""
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
    
    tk.Label(   frame_esquerda, 
                text="Início", 
                font=pattern.fonte_cabecalho_22, 
                fg=pattern.cor_fria_paleta
            ).pack(side='bottom', pady=10)

    def Apagar_Nivel():
        """Abre janela de confirmação para apagar o nível atual."""
        def Limpar_Pagina_Meus_Niveis():
            """Limpa e atualiza a página de níveis após exclusão."""
            Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, pagina)
            janela_nivel.destroy()

        Exibir_Janela_Apagar_Nivel(pagina, nivel_id, lambda: Limpar_Pagina_Meus_Niveis())

    tk.Button(frame_esquerda, 
text="Apagar nível", 
font=pattern.fonte_cabecalho_12, 
bg=pattern.cor_quente_paleta, 
fg=pattern.cor_fonte_padrao,
command=lambda: Apagar_Nivel()
).pack(side='top', pady=10)

    tk.Label(   frame_direita, 
                text="Fim", 
                font=pattern.fonte_cabecalho_22, 
                fg=pattern.cor_quente_paleta
            ).pack(side='top', pady=10)

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
        """Atualiza as imagens das peças após o redimensionamento da janela."""
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
    """
    Gera a página principal para gerenciamento dos níveis do usuário.
    
    Parameters:
        raiz (tk.Tk): Janela principal da aplicação
    
    Global:
        Atualiza a variável global Usuario_Atual
    
    Returns:
        None
    """
    global Usuario_Atual
    Usuario_Atual = Obter_Usuario_Atual()

    pagina = tk.Toplevel(raiz)
    pagina.transient(raiz)
    pagina.grab_set()
    pagina.focus_force()

    def ao_fechar_pagina_niveis():
        """Fecha a página de níveis e libera o controle da janela principal."""
        pagina.destroy()
        raiz.focus_force()
        raiz.grab_release()  # Libera o grab da janela principal
    
    pagina.protocol("WM_DELETE_WINDOW", ao_fechar_pagina_niveis)

    pagina.title("Meus níveis")
    pagina.geometry("800x400")

    Centralizar_Janela(pagina)

    label = tk.Label(   pagina, 
                        text="Meus níveis", 
                        font=pattern.fonte_cabecalho_22,
                        fg=pattern.cor_fonte_padrao)
    label.pack(pady=20)

    frame_niveis = tk.Frame(pagina)
    frame_niveis.pack(pady=20, fill='both', expand=True)

    frame_botoes_avancar_recuar = tk.Frame(pagina)
    frame_botoes_avancar_recuar.pack(pady=20, fill='both', expand=True)

    frame_niveis_superior = tk.Frame(frame_niveis)
    frame_niveis_superior.pack(fill='x', pady=5, expand=True)

    frame_niveis_inferior = tk.Frame(frame_niveis)
    frame_niveis_inferior.pack(fill='x', pady=5, expand=True)

    botao_recuar = tk.Button(frame_botoes_avancar_recuar, text='<', fg=pattern.cor_branca_paleta, bg='#3b68ff', 
                                        font=pattern.fonte_cabecalho_11, command=lambda: Recuar_Exibicao_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg=pattern.cor_branca_paleta, bg='#ff3b3b', 
                                        font=pattern.fonte_cabecalho_11, command=lambda: Avancar_Exibicao_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Meus_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina)

    pagina.mainloop()

def Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, janela_niveis):
    """
    Limpa e recria os botões de níveis nos frames especificados.
    
    Parameters:
        frame_sup (tk.Frame): Frame superior para exibição de botões
        frame_inf (tk.Frame): Frame inferior para exibição de botões
        janela_niveis (tk.Toplevel): Janela de níveis para callback
    
    Returns:
        None
    """
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
        fg = pattern.cor_fonte_niveis
        match (nivel['dificuldade'].upper()):
            case 'FACIL': bg = pattern.verde 
            case 'MEDIO': bg = pattern.amarelo
            case 'DIFICIL': bg = pattern.vermelho

        if botoes_no_frame_superior < 5:
            nivel_button = tk.Button(frame_sup, 
                                    text=nivel['nome'], 
                                    height=2, bg=bg, 
                                    fg=fg, 
                                    font=pattern.fonte_cabecalho_12,
                                    command=lambda p_nivelid = nivel['id']: Exibir_Meu_Nivel(p_nivelid, janela_niveis, frame_sup, frame_inf))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(frame_inf, 
                                    text=nivel['nome'], 
                                    height=2, 
                                    bg=bg, 
                                    fg=fg, 
                                    font=pattern.fonte_cabecalho_12,
                                    command=lambda p_nivelid = nivel['id']: Exibir_Meu_Nivel(p_nivelid, janela_niveis, frame_sup, frame_inf))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: break

def Avancar_Exibicao_Meus_Niveis(frame_sup, frame_inf, janela_raiz):
    """
    Avança para a próxima página de exibição de níveis.
    
    Parameters:
        frame_sup (tk.Frame): Frame superior para atualização
        frame_inf (tk.Frame): Frame inferior para atualização
        janela_raiz (tk.Toplevel): Janela principal de níveis
    
    Global:
        Modifica controle_meus_niveis_exibidos
    
    Returns:
        None
    """
    global controle_meus_niveis_exibidos

    quantidade_niveis_existente = len(crud.Buscar_Niveis_Do_Usuario(Usuario_Atual['usuario']))

    quantidade_niveis_exibidos_nesse_momento = controle_meus_niveis_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_niveis_existente):
        return

    controle_meus_niveis_exibidos[0] += 10
    controle_meus_niveis_exibidos[1] += 10
    Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, janela_raiz)

def Recuar_Exibicao_Meus_Niveis(frame_sup, frame_inf, janela_raiz):
    """
    Retorna para a página anterior de exibição de níveis.
    
    Parameters:
        frame_sup (tk.Frame): Frame superior para atualização
        frame_inf (tk.Frame): Frame inferior para atualização
        janela_raiz (tk.Toplevel): Janela principal de níveis
    
    Global:
        Modifica controle_meus_niveis_exibidos
    
    Returns:
        None
    """
    global controle_meus_niveis_exibidos
    if (controle_meus_niveis_exibidos[0] - 10 < 0):
        return

    controle_meus_niveis_exibidos[0] -= 10
    controle_meus_niveis_exibidos[1] -= 10
    Limpar_Exibir_Botoes_Meus_Niveis(frame_sup, frame_inf, janela_raiz)

def Calcular_Tamanho_Janela(matriz):
    """
    Calcula o tamanho ideal da janela baseado na matriz de peças.
    
    Parameters:
        matriz (list): Matriz 2D representando a estrutura do nível
    
    Returns:
        tuple: (largura_total, altura_total, tamanho_celula)
               - largura_total: Largura total da janela em pixels
               - altura_total: Altura total da janela em pixels  
               - tamanho_celula: Tamanho de cada célula em pixels
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
    """
    Exibe janela de confirmação para exclusão de nível com verificação de senha.
    
    Parameters:
        raiz (tk.Tk): Janela pai
        nivel_id (int): ID do nível a ser excluído
        callback (function, optional): Função a ser executada após exclusão
    
    Returns:
        None
    """
    janela_confirmacao = tk.Toplevel(raiz)
    janela_confirmacao.transient(raiz)
    janela_confirmacao.grab_set()
    janela_confirmacao.focus_force()

    def ao_fechar_janela():
        """Fecha a janela de confirmação e retorna o foco para a janela pai."""
        janela_confirmacao.destroy()
        raiz.grab_set()
        raiz.focus_force()

    janela_confirmacao.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    def Excluir_Nivel():
        """Executa a exclusão do nível após validação da senha."""
        senha = senha_entry.get()
        if not senha or codifier.Codificar_Senha(senha) != Obter_Usuario_Atual()['senha']:
            messagebox.showerror("Opss", "Senha incorreta!")
            return
        crud.Excluir_Nivel(nivel_id)
        messagebox.showinfo("Sucesso", "Nível excluído com sucesso!")
        ao_fechar_janela()
        if callback:
            callback()

    tk.Label(   janela_confirmacao, 
                text='Confirme sua senha: ',
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao
            ).grid(row=0, column=0, padx=5, pady=5)

    senha_entry = tk.Entry( janela_confirmacao, 
                            show='*',
                            font=pattern.fonte_texto,
                            fg=pattern.cor_fonte_padrao)
    senha_entry.grid(row=0, column=1, padx=5, pady=5)
    senha_entry.focus()
    senha_entry.bind('<Return>', lambda e: Excluir_Nivel())

    tk.Button(  janela_confirmacao, 
                text='Cancelar',
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta, 
                command=lambda: ao_fechar_janela()
            ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(janela_confirmacao, 
                text='Confirmar',
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao,
                bg=pattern.cor_fria_paleta,
                command=lambda: Excluir_Nivel()
            ).grid(row=1, column=1, padx=5, pady=5)

    Centralizar_Janela(janela_confirmacao)
    janela_confirmacao.mainloop()