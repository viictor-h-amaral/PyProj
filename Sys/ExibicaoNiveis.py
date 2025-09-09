from pathlib import Path
import Sys.Crud as crud
import Sys.LevelRunner as LRunner
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Sys.Login import Obter_Usuario_Atual, Atualizar_Usuario_Atual

Nivel = None
Estrutura = None
Matriz_Estrutural = None
controle_niveis_exibidos = [0, 10]

Usuario_Atual = None

Nivel_Atual_Concluido = False

def Exibir_Nivel(nivel_id, raiz):
    global Usuario_Atual, Nivel
    
    Nivel = crud.Buscar_Nivel(nivel_id)
    
    if crud.Retornar_Se_Nivel_Concluido(Usuario_Atual, nivel_id): 
        Exibir_Nivel_Concluido(nivel_id, raiz)
    else: 
        Exibir_Nivel_Incompleto(nivel_id, raiz)

def Exibir_Nivel_Concluido(nivel_id, pagina):
    global Estrutura, Matriz_Estrutural, Nivel_Atual_Concluido

    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]
    
    # Calcula tamanho automático da janela
    largura_janela, altura_janela, tamanho_celula = Calcular_Tamanho_Janela(Matriz_Estrutural)
    
    raiz = tk.Toplevel(pagina)
    raiz.transient(pagina)
    raiz.grab_set()
    raiz.focus_force()

    def ao_fechar_nivel_concluido():
        raiz.destroy()
        pagina.focus_force()
        pagina.grab_set()
    
    raiz.protocol("WM_DELETE_WINDOW", ao_fechar_nivel_concluido)

    raiz.title(f"Nível Concluído {nivel_id}")
    raiz.geometry(f'{largura_janela}x{altura_janela}')
    raiz.resizable(False, False)
    
    num_linhas = len(Matriz_Estrutural)
    num_colunas = len(Matriz_Estrutural[0])
    
    # Configuração similar
    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_columnconfigure(1, weight=1)
    
    frame_esquerda = tk.Frame(raiz, width=100)
    frame_direita = tk.Frame(raiz, width=100)
    frame_nivel = tk.Frame(raiz)
    
    frame_esquerda.grid(row=0, column=0, sticky='ns')
    frame_nivel.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
    frame_direita.grid(row=0, column=2, sticky='ns')
    
    for i in range(num_linhas):
        frame_nivel.grid_rowconfigure(i, weight=1, uniform="peca_row")
    for j in range(num_colunas):
        frame_nivel.grid_columnconfigure(j, weight=1, uniform="peca_col")
    
    tk.Label(frame_esquerda, text="Início", font=("Arial", 14), fg='green').pack(side='bottom', pady=10)
    tk.Label(frame_direita, text="Fim", font=("Arial", 14), fg='red').pack(side='top', pady=10)
    
    janela_nivel = frame_nivel
    janela_nivel.imagens_pecas = []
    
    # Cria botões desabilitados primeiro
    botoes = {}
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):
            botao = tk.Button(janela_nivel, state='disabled')
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            botoes[(indice_linha, indice_coluna)] = botao
    
    # Função para atualizar imagens após renderização
    def atualizar_imagens_concluido():
        if botoes:
            primeiro_botao = list(botoes.values())[0]
            primeiro_botao.update_idletasks()
            largura_botao = primeiro_botao.winfo_width()
            altura_botao = primeiro_botao.winfo_height()
            
            tamanho_imagem = min(largura_botao, altura_botao) - 4
            
            for (linha, coluna), botao in botoes.items():
                peca_id = Matriz_Estrutural[linha][coluna]
                imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
                janela_nivel.imagens_pecas.append(imagem_peca)
                botao.config(image=imagem_peca, state='disabled')
                botao.image = imagem_peca
    
    raiz.after(100, atualizar_imagens_concluido)

    raiz.mainloop()

def Exibir_Nivel_Incompleto(nivel_id, pagina):
    global Estrutura, Matriz_Estrutural, Nivel_Atual_Concluido

    Estrutura = crud.Buscar_Estrutura_Do_Nivel(nivel_id)
    Matriz_Estrutural = Estrutura["matriz_pecas"]
    
    # Calcula tamanho automático da janela
    largura_janela, altura_janela, tamanho_celula = Calcular_Tamanho_Janela(Matriz_Estrutural)
    
    raiz = tk.Toplevel(pagina)
    raiz.transient(pagina)
    raiz.grab_set()
    raiz.focus_force()

    def ao_fechar_nivel_incompleto():
        raiz.destroy()
        pagina.focus_force()
        pagina.grab_set()
    
    raiz.protocol("WM_DELETE_WINDOW", ao_fechar_nivel_incompleto)

    raiz.title(f"Nível {nivel_id}")
    raiz.geometry(f'{largura_janela}x{altura_janela}')
    raiz.resizable(False, False)
    
    num_linhas = len(Matriz_Estrutural)
    num_colunas = len(Matriz_Estrutural[0])
    
    # Configura o grid principal
    raiz.grid_rowconfigure(0, weight=1)
    raiz.grid_columnconfigure(1, weight=1)
    
    # Frame para labels laterais
    frame_esquerda = tk.Frame(raiz, width=100)
    frame_direita = tk.Frame(raiz, width=100)
    
    # Frame principal para o nível
    frame_nivel = tk.Frame(raiz)
    
    frame_esquerda.grid(row=0, column=0, sticky='ns')
    frame_nivel.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
    frame_direita.grid(row=0, column=2, sticky='ns')
    
    # Configura grid do frame do nível para expandir uniformemente
    for i in range(num_linhas):
        frame_nivel.grid_rowconfigure(i, weight=1, uniform="peca_row")
    for j in range(num_colunas):
        frame_nivel.grid_columnconfigure(j, weight=1, uniform="peca_col")
    
    # Labels de início e fim
    tk.Label(frame_esquerda, text="Início", font=("Arial", 14), fg='green').pack(side='bottom', pady=10)
    tk.Label(frame_direita, text="Fim", font=("Arial", 14), fg='red').pack(side='top', pady=10)
    
    # Mantém referência às imagens
    janela_nivel = frame_nivel
    janela_nivel.botoes_pecas = {}
    janela_nivel.pecas_ids = LRunner.Embaralhar_Pecas(Matriz_Estrutural)
    janela_nivel.imagens_pecas = []
    
    # Primeiro, cria todos os botões vazios para poder calcular seus tamanhos
    for indice_linha in range(num_linhas):
        for indice_coluna in range(num_colunas):
            botao = tk.Button(janela_nivel)
            botao.grid(row=indice_linha, column=indice_coluna, sticky='nsew', padx=1, pady=1)
            janela_nivel.botoes_pecas[(indice_linha, indice_coluna)] = botao
    
    # Função para atualizar as imagens após a janela ser renderizada
    def atualizar_imagens():
        # Obtém o tamanho real dos botões após o grid ser calculado
        if janela_nivel.botoes_pecas:
            primeiro_botao = list(janela_nivel.botoes_pecas.values())[0]
            primeiro_botao.update_idletasks()  # Força atualização
            largura_botao = primeiro_botao.winfo_width()
            altura_botao = primeiro_botao.winfo_height()
            
            # Usa o menor lado para manter aspecto quadrado, mas subtrai um pouco para margem
            tamanho_imagem = min(largura_botao, altura_botao) - 2  # -4 pixels para margem
            
            for (linha, coluna), botao in janela_nivel.botoes_pecas.items():
                peca_id = janela_nivel.pecas_ids[linha][coluna]
                
                # Cria imagem com tamanho calculado
                imagem_peca = LRunner.Buscar_Imagem_Peca(peca_id, (tamanho_imagem, tamanho_imagem))
                janela_nivel.imagens_pecas.append(imagem_peca)
                
                # Configura o botão com a imagem
                botao.config(
                    image=imagem_peca,
                    command=lambda l=linha, c=coluna: Rotina_Clique_Peca((l, c), janela_nivel)
                )
                botao.image = imagem_peca  # Mantém referência
    
    # Agenda a atualização das imagens após a janela ser renderizada
    raiz.after(5, atualizar_imagens)

    raiz.mainloop()


def Rotina_Clique_Peca(coordenada, janela_nivel):
    LRunner.Atualizar_Peca(coordenada, janela_nivel)
    Rotina_Valida_Nivel(janela_nivel)
    
def Rotina_Valida_Nivel(janela):
    global Nivel_Atual_Concluido

    nivel_concluido = LRunner.Rotina_Verifica_Nivel_Valido(janela.pecas_ids)
    if nivel_concluido: 
        if (not Nivel_Atual_Concluido): 
            Rotina_Nivel_Concluido(janela)
            messagebox.showinfo("Sucesso", "Nível concluído!")
        Nivel_Atual_Concluido = True
    else: Nivel_Atual_Concluido = False

def Rotina_Nivel_Concluido(janela):
    global Nivel
    global Usuario_Atual

    for widget in janela.winfo_children():
        widget.configure(state='disabled')

    crud.Salvar_Nivel_Concluido(Usuario_Atual, Nivel)
    Usuario_Atual = Atualizar_Usuario_Atual()  
    x = 2

def Gerar_Pagina_Niveis(raiz):

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

    botao_recuar = tk.Button(frame_botoes_avancar_recuar, text='<', fg='white', bg='#3b68ff', 
                                        font=('Arial', 16), command=lambda: Recuar_Exibicao_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg='white', bg='#ff3b3b', 
                                        font=('Arial', 16), command=lambda: Avancar_Exibicao_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Niveis(frame_niveis_superior, frame_niveis_inferior, pagina)

    pagina.mainloop()

def Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf, janela_niveis):
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
        bg = 'white'
        fg = 'black'
        match (nivel['dificuldade'].upper()):
            case 'FACIL': bg = '#a3ffa8' 
            case 'MEDIO': bg = '#fcffa3'
            case 'DIFICIL': bg = '#ff8787'

        if botoes_no_frame_superior < 5:
            nivel_button = tk.Button(frame_sup, text=nivel['nome'], height=2, bg = bg, fg=fg, font=('Arial', 9, 'bold'),
                                   command=lambda p_nivelid=nivel['id']: Exibir_Nivel(p_nivelid, janela_niveis))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(frame_inf, text=nivel['nome'], height=2, bg = bg, fg=fg, font=('Arial', 9, 'bold'),
                                   command=lambda p_nivelid=nivel['id']: Exibir_Nivel(p_nivelid, janela_niveis))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: 
            break

def Recuar_Exibicao_Niveis(frame_sup, frame_inf, raiz):
    global controle_niveis_exibidos
    if (controle_niveis_exibidos[0] - 10 < 0):
        return

    controle_niveis_exibidos[0] -= 10
    controle_niveis_exibidos[1] -= 10
    Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf, raiz)

def Avancar_Exibicao_Niveis(frame_sup, frame_inf, raiz):
    global controle_niveis_exibidos

    quantidade_niveis_existente = len(crud.Buscar_Niveis())

    quantidade_niveis_exibidos_nesse_momento = controle_niveis_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_niveis_existente):
        return

    controle_niveis_exibidos[0] += 10
    controle_niveis_exibidos[1] += 10
    Limpar_Exibir_Botoes_Niveis(frame_sup, frame_inf, raiz)

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

def Buscar_Imagem_Peca_Redimensionada(peca_id, tamanho):
    """
    Versão modificada da Buscar_Imagem_Peca que aceita tamanho personalizado
    """
    arquivo_img = crud.Buscar_Peca_Arquivo(peca_id)
    end_img = LRunner.Endereco_Imagem(arquivo_img)
    
    img = Image.open(end_img)
    img = img.resize((tamanho, tamanho), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)
