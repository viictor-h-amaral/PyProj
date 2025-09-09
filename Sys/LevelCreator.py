import tkinter as tk
from tkinter import messagebox
from Sys.Login import Centralizar_Janela

num_linhas = None
num_colunas = None

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
        ao_fechar_janela()

    tk.Button(frame_botoes, text='Criar nível', command= lambda: Salvar_Dimensoes(), width=10).pack(side='right', padx=5)
    tk.Button(frame_botoes, text='Cancelar', command= lambda: ao_fechar_janela(), width=10).pack(side='right', padx=5)

    Centralizar_Janela(janela)
    janela.mainloop()
