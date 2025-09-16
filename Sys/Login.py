"""
Módulo de gerenciamento de login e usuários para uma aplicação Tkinter.

Este módulo fornece:
- Tela de login
- Criação de novos usuários
- Exclusão de usuários
- Validação de credenciais
- Controle do usuário logado
- Logout automático
- Garantia de existência de arquivo de usuários

Dependências:
    - tkinter (para interface gráfica)
    - json (para manipulação de dados)
    - Sys.Crud (módulo customizado de persistência de dados)
    - Sys.Codifier (módulo customizado para criptografia de senhas)
    - Sys.WindowsPattern (módulo com estilos visuais, fontes e cores)
"""

import tkinter as tk
from tkinter import messagebox
import json
import Sys.Crud as crud
import Sys.Codifier as codifier
import Sys.WindowsPattern as pattern

# Variáveis globais de estado
usuario_atual = None              # Guarda o usuário atualmente logado
callback_login_sucesso = None     # Função callback executada após login bem-sucedido
janela_login = None               # Referência da janela de login aberta


def Inicializar_Sistema_Login(raiz, callback_sucesso):
    """
    Inicializa o sistema de login.

    Args:
        raiz (tk.Tk): Janela principal da aplicação.
        callback_sucesso (function): Função executada após login bem-sucedido.
    """
    global callback_login_sucesso
    callback_login_sucesso = callback_sucesso
    Mostrar_Janela_Login(raiz)


def Garantir_Arquivo_Usuario_Existe():
    """
    Garante que o arquivo de usuários JSON exista.
    Caso não exista, cria um arquivo com o usuário padrão 'admin'.
    """
    arquivo_usuario = crud.Obter_Caminho_Arquivo('Usuarios.json')
    if not arquivo_usuario.exists():
        arquivo_usuario.parent.mkdir(exist_ok=True)
        with open(arquivo_usuario, 'w', encoding='utf-8') as f:
            usuario_padrao = [{
                'id': 1,
                'usuario': 'admin',
                'senha': codifier.Codificar_Senha('admin'),
                'papel': 'admin'
            }]
            json.dump(usuario_padrao, f, indent=4)


def Validar_Credenciais(usuario, senha):
    """
    Valida as credenciais de um usuário.

    Args:
        usuario (str): Nome do usuário.
        senha (str): Senha em texto plano.

    Returns:
        dict | None: Dicionário com dados do usuário se válido, caso contrário None.
    """
    usuarios = crud.Carregar_Usuarios()
    senha_codificada = codifier.Codificar_Senha(senha)
    
    for user in usuarios:
        if user['usuario'] == usuario and user['senha'] == senha_codificada:
            return user
    return None


def Criar_Novo_Usuario(usuario, senha, papel):
    """
    Cria um novo usuário no sistema.

    Args:
        usuario (str): Nome de usuário único.
        senha (str): Senha em texto plano.
        papel (str): Tipo do usuário ("admin" ou "user").

    Returns:
        tuple: (bool, str) indicando sucesso e mensagem.
    """
    usuarios = crud.Carregar_Usuarios()
    
    if any(user['usuario'] == usuario for user in usuarios):
        return False, "Usuário já existente"
    
    novo_usuario = {
        'id': crud.Gerar_Id(usuarios),
        'usuario': usuario,
        'senha': codifier.Codificar_Senha(senha),
        'papel': papel,
        'niveis_concluidos': []
    }
    
    usuarios.append(novo_usuario)
    crud.Salvar_Usuarios(usuarios)
    return True, "Usuário criado com sucesso"


def Apagar_Usuario(raiz, usuario):
    """
    Exibe uma janela de confirmação para exclusão de um usuário.

    Args:
        raiz (tk.Tk): Janela principal da aplicação.
        usuario (dict): Usuário que será excluído.
    """
    janela_confirmacao = tk.Toplevel(raiz)
    janela_confirmacao.transient(raiz)
    janela_confirmacao.grab_set()
    janela_confirmacao.focus_force()

    def ao_fechar_janela():
        janela_confirmacao.destroy()
        raiz.grab_set()
        raiz.focus_force()

    janela_confirmacao.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    def Excluir_Usuario():
        senha = senha_entry.get()
        if not senha or codifier.Codificar_Senha(senha) != usuario['senha']:
            messagebox.showerror("Opss", "Senha incorreta!")
            return
        crud.Excluir_Usuario(usuario)
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
        ao_fechar_janela()
        Fazer_Logout(raiz)

    # Layout da janela de confirmação
    tk.Label(janela_confirmacao, text='Confirme sua senha: ',
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=0, column=0, padx=5, pady=5)

    senha_entry = tk.Entry(janela_confirmacao, show='*',
                           font=pattern.fonte_texto,
                           fg=pattern.cor_fonte_padrao)
    senha_entry.grid(row=0, column=1, padx=5, pady=5)
    senha_entry.focus()
    senha_entry.bind('<Return>', lambda: Excluir_Usuario())

    tk.Button(janela_confirmacao, text='Cancelar',
              font=pattern.fonte_cabecalho_12,
              fg=pattern.cor_fonte_clara,
              bg=pattern.cor_escura_paleta,
              width=15,
              command=ao_fechar_janela).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(janela_confirmacao, text='Confirmar',
              font=pattern.fonte_cabecalho_12,
              fg=pattern.cor_fonte_padrao,
              bg=pattern.cor_fria_paleta,
              width=15,
              command=Excluir_Usuario).grid(row=1, column=1, padx=5, pady=5)

    Centralizar_Janela(janela_confirmacao)
    janela_confirmacao.mainloop()


def Tentar_Login(entrada_usuario, entrada_senha, raiz):
    """
    Tenta realizar login com os dados fornecidos.

    Args:
        entrada_usuario (tk.Entry): Campo de usuário.
        entrada_senha (tk.Entry): Campo de senha.
        raiz (tk.Tk): Janela principal.
    """
    global usuario_atual, janela_login
    
    usuario = entrada_usuario.get().strip()
    senha = entrada_senha.get().strip()
    
    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return
    
    user = Validar_Credenciais(usuario, senha)
    if user:
        usuario_atual = user
        janela_login.destroy()
        if callback_login_sucesso:
            callback_login_sucesso(user)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")
        entrada_senha.delete(0, tk.END)


def Mostrar_Janela_Novo_Usuario(entrada_usuario, entrada_senha):
    """
    Mostra a janela para criação de um novo usuário.

    Args:
        entrada_usuario (tk.Entry): Campo de entrada da tela de login.
        entrada_senha (tk.Entry): Campo de senha da tela de login.
    """
    global janela_login
    
    janela_novo = tk.Toplevel(janela_login)
    janela_novo.title("Novo Usuário")
    janela_novo.geometry("400x200")
    janela_novo.resizable(False, False)
    janela_novo.transient(janela_login)
    janela_novo.grab_set()
    
    Centralizar_Janela(janela_novo)
    
    frame = tk.Frame(janela_novo)
    frame.grid(row=0, column=0, padx=5, pady=5)
    
    tk.Label(frame, text="Novo Usuário: ",
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=0, column=0, sticky='w', pady=(0, 5))

    entrada_novo_user = tk.Entry(frame, width=20,
                                 font=pattern.fonte_texto,
                                 fg=pattern.cor_fonte_padrao)
    entrada_novo_user.grid(row=0, column=1, pady=(0, 5))
    entrada_novo_user.focus()
    
    tk.Label(frame, text="Nova Senha: ",
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=1, column=0, sticky='w', pady=(0, 5))

    entrada_nova_senha = tk.Entry(frame, width=20, show='*',
                                  font=pattern.fonte_texto,
                                  fg=pattern.cor_fonte_padrao)
    entrada_nova_senha.grid(row=1, column=1, pady=(0, 5))
    
    tk.Label(frame, text="Confirmar Senha:",
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=2, column=0, sticky='w', pady=(0, 10))

    entrada_conf_senha = tk.Entry(frame, width=20, show='*',
                                  font=pattern.fonte_texto,
                                  fg=pattern.cor_fonte_padrao)
    entrada_conf_senha.grid(row=2, column=1, pady=(0, 10))

    frame_papel = tk.Frame(janela_novo)
    frame_papel.grid(row=1, column=0)

    tk.Label(frame_papel, text="Papel:",
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=0, column=0, sticky='w', pady=(0, 10))

    papel_novo_usuario = tk.StringVar(value="user")
    radio_adm = tk.Radiobutton(frame_papel, text="Administrador",
                               font=pattern.fonte_texto,
                               fg=pattern.cor_fonte_padrao,
                               variable=papel_novo_usuario, value="admin")
    radio_adm.grid(row=0, column=1)

    radio_user = tk.Radiobutton(frame_papel, text="Player",
                                font=pattern.fonte_texto,
                                fg=pattern.cor_fonte_padrao,
                                variable=papel_novo_usuario, value="user")
    radio_user.grid(row=0, column=2)

    def Executar_Criar_Usuario():
        usuario = entrada_novo_user.get().strip()
        senha = entrada_nova_senha.get().strip()
        confirmar_senha = entrada_conf_senha.get().strip()
        papel = papel_novo_usuario.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "Senhas não coincidem")
            return
        
        sucesso, mensagem = Criar_Novo_Usuario(usuario, senha, papel)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            janela_novo.destroy()
            entrada_usuario.delete(0, tk.END)
            entrada_senha.delete(0, tk.END)
            entrada_usuario.insert(0, usuario)
            entrada_senha.focus()
        else:
            messagebox.showerror("Erro", mensagem)
    
    frame_botoes = tk.Frame(janela_novo)
    frame_botoes.grid(row=2, column=0, pady=5, padx=5)
    
    tk.Button(frame_botoes, text="Criar",
              font=pattern.fonte_cabecalho_12,
              fg=pattern.cor_fonte_padrao,
              bg=pattern.cor_fria_paleta,
              command=Executar_Criar_Usuario,
              width=10).pack(side='right', padx=5)

    tk.Button(frame_botoes, text="Cancelar",
              font=pattern.fonte_cabecalho_12,
              fg=pattern.cor_fonte_clara,
              bg=pattern.cor_escura_paleta,
              command=janela_novo.destroy,
              width=10).pack(side='left', padx=5)


def Centralizar_Janela(janela):
    """Centraliza uma janela na tela."""
    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def Cancelar_Login(raiz):
    """Cancela o login e fecha a aplicação."""
    global janela_login
    janela_login.destroy()
    raiz.destroy()


def Mostrar_Janela_Login(raiz):
    """
    Exibe a janela de login.

    Args:
        raiz (tk.Tk): Janela principal da aplicação.
    """
    global janela_login
    raiz.withdraw()
    Garantir_Arquivo_Usuario_Existe()
    
    janela_login = tk.Toplevel(raiz)
    janela_login.title("Login")
    janela_login.geometry("380x150")
    janela_login.resizable(False, False)
    janela_login.grab_set()
    janela_login.focus_force()
    
    Centralizar_Janela(janela_login)
    
    frame = tk.Frame(janela_login)
    frame.grid(row=0, column=0, padx=5, pady=15)
    
    tk.Label(frame, text="Usuário: ",
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=0, column=0, sticky='w', pady=(0, 5))

    entrada_usuario = tk.Entry(frame, width=20,
                               font=pattern.fonte_texto,
                               fg=pattern.cor_fonte_padrao)
    entrada_usuario.grid(row=0, column=1, pady=(0, 5))
    entrada_usuario.focus_force()
    
    tk.Label(frame, text="Senha: ",
             font=pattern.fonte_cabecalho_12,
             fg=pattern.cor_fonte_padrao).grid(row=1, column=0, sticky='w', pady=(0, 10))

    entrada_senha = tk.Entry(frame, width=20, show='*',
                             font=pattern.fonte_texto,
                             fg=pattern.cor_fonte_padrao)
    entrada_senha.grid(row=1, column=1, pady=(0, 10))
    
    frame_botoes = tk.Frame(janela_login)
    frame_botoes.grid(row=1, column=0, pady=5, padx=5)
    
    tk.Button(frame_botoes, text="Login",
              font=pattern.fonte_cabecalho_11,
              fg=pattern.cor_fonte_clara,
              bg=pattern.cor_quente_paleta,
              command=lambda: Tentar_Login(entrada_usuario, entrada_senha, raiz)
              ).pack(side='right', padx=5)

    tk.Button(frame_botoes, text="Novo Usuário",
              font=pattern.fonte_cabecalho_11,
              fg=pattern.cor_fonte_padrao,
              bg=pattern.cor_fria_paleta,
              command=lambda: Mostrar_Janela_Novo_Usuario(entrada_usuario, entrada_senha)
              ).pack(side='right', padx=5)

    tk.Button(frame_botoes, text="Cancelar",
              font=pattern.fonte_cabecalho_11,
              fg=pattern.cor_fonte_clara,
              bg=pattern.cor_escura_paleta,
              command=lambda: Cancelar_Login(raiz)
              ).pack(side='left', padx=5)
    
    entrada_senha.bind('<Return>', lambda e: Tentar_Login(entrada_usuario, entrada_senha, raiz))


def Obter_Usuario_Atual():
    """Retorna o usuário atualmente logado."""
    usuario_atual = Atualizar_Usuario_Atual()
    return usuario_atual


def Atualizar_Usuario_Atual():
    """Recarrega os dados do usuário atual a partir do arquivo JSON."""
    return crud.Carregar_Usuario(usuario_atual['usuario'])


def Fazer_Logout(raiz, callback_logout=None):
    """
    Realiza logout do usuário atual.

    Args:
        raiz (tk.Tk): Janela principal.
        callback_logout (function, opcional): Função a ser chamada no logout.
    """
    global usuario_atual, janela_login
    usuario_atual = None
    if callback_logout:
        callback_logout()
    
    for widget in raiz.winfo_children():
        widget.destroy()
    
    Mostrar_Janela_Login(raiz)
