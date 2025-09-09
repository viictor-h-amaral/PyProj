import tkinter as tk
from tkinter import messagebox
import json
import Sys.Crud as crud
import Sys.Codificador as codificador

# Configurações de estilo
FONTE_PADRAO = "Roboto"
COR_PRIMARIA = "#6366f1"
COR_SECUNDARIA = "#818cf8"
COR_ACENTO = "#f471b5"
COR_TEXTO = "#1e293b"
COR_FUNDO = "#f1f5f9"

usuario_atual = None
callback_login_sucesso = None
janela_login = None

def inicializar_sistema_login(janela_raiz, callback_sucesso):
    global callback_login_sucesso
    callback_login_sucesso = callback_sucesso
    mostrar_janela_login(janela_raiz)

def garantir_arquivo_usuario_existe():
    caminho_arquivo = crud.obter_caminho_arquivo('Usuarios.json')
    if not caminho_arquivo.exists():
        caminho_arquivo.parent.mkdir(exist_ok=True)
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            usuario_admin = [{
                'id': 1,
                'usuario': 'admin',
                'senha': codificador.codificar_senha('admin'),
                'papel': 'admin',
                'niveis_concluidos': []
            }]
            json.dump(usuario_admin, arquivo, indent=4, ensure_ascii=False)

def validar_credenciais(usuario, senha):
    usuarios = crud.carregar_usuarios()
    senha_codificada = codificador.codificar_senha(senha)
    
    for user in usuarios:
        if user['usuario'] == usuario and user['senha'] == senha_codificada:
            return user
    return None

def criar_novo_usuario(usuario, senha, papel):
    usuarios = crud.carregar_usuarios()
    
    if any(user['usuario'] == usuario for user in usuarios):
        return False, "Usuário já existe"
    
    novo_usuario = {
        'id': len(usuarios) + 1,
        'usuario': usuario,
        'senha': codificador.codificar_senha(senha),
        'papel': papel,
        'niveis_concluidos': []
    }
    
    usuarios.append(novo_usuario)
    crud.salvar_usuarios(usuarios)
    return True, "Usuário criado com sucesso"

def tentar_login(entrada_usuario, entrada_senha, janela_raiz):
    global usuario_atual, janela_login
    
    usuario = entrada_usuario.get().strip()
    senha = entrada_senha.get().strip()
    
    if not usuario or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return
    
    usuario_encontrado = validar_credenciais(usuario, senha)
    if usuario_encontrado:
        usuario_atual = usuario_encontrado
        janela_login.destroy()
        if callback_login_sucesso:
            callback_login_sucesso(usuario_encontrado)
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")
        entrada_senha.delete(0, tk.END)

def mostrar_janela_novo_usuario(entrada_usuario, entrada_senha):
    global janela_login
    
    janela_novo_usuario = tk.Toplevel(janela_login)
    janela_novo_usuario.title("Novo Usuário")
    janela_novo_usuario.geometry("350x250")
    janela_novo_usuario.resizable(False, False)
    janela_novo_usuario.configure(bg=COR_FUNDO)
    janela_novo_usuario.transient(janela_login)
    janela_novo_usuario.grab_set()
    
    centralizar_janela(janela_novo_usuario)
    
    frame_principal = tk.Frame(janela_novo_usuario, padx=25, pady=25, bg=COR_FUNDO)
    frame_principal.pack(expand=True, fill='both')
    
    tk.Label(
        frame_principal, 
        text="Novo Usuário:", 
        bg=COR_FUNDO, 
        fg=COR_TEXTO,
        font=(FONTE_PADRAO, 10)
    ).grid(row=0, column=0, sticky='w', pady=(0, 5))
    
    entrada_novo_usuario = tk.Entry(
        frame_principal, 
        width=22, 
        font=(FONTE_PADRAO, 10)
    )
    entrada_novo_usuario.grid(row=0, column=1, pady=(0, 5))
    entrada_novo_usuario.focus()
    
    tk.Label(
        frame_principal, 
        text="Nova Senha:", 
        bg=COR_FUNDO, 
        fg=COR_TEXTO,
        font=(FONTE_PADRAO, 10)
    ).grid(row=1, column=0, sticky='w', pady=(0, 5))
    
    entrada_nova_senha = tk.Entry(
        frame_principal, 
        width=22, 
        show='*',
        font=(FONTE_PADRAO, 10)
    )
    entrada_nova_senha.grid(row=1, column=1, pady=(0, 5))
    
    tk.Label(
        frame_principal, 
        text="Confirmar Senha:", 
        bg=COR_FUNDO, 
        fg=COR_TEXTO,
        font=(FONTE_PADRAO, 10)
    ).grid(row=2, column=0, sticky='w', pady=(0, 10))
    
    entrada_confirmar_senha = tk.Entry(
        frame_principal, 
        width=22, 
        show='*',
        font=(FONTE_PADRAO, 10)
    )
    entrada_confirmar_senha.grid(row=2, column=1, pady=(0, 10))

    papel_variavel = tk.StringVar(value="user")
    
    tk.Radiobutton(
        frame_principal, 
        text="Administrador", 
        variable=papel_variavel, 
        value="admin",
        bg=COR_FUNDO,
        font=(FONTE_PADRAO, 9)
    ).grid(row=3, column=0)
    
    tk.Radiobutton(
        frame_principal, 
        text="Jogador", 
        variable=papel_variavel, 
        value="user",
        bg=COR_FUNDO,
        font=(FONTE_PADRAO, 9)
    ).grid(row=3, column=1)

    def executar_criar_usuario():
        nome_usuario = entrada_novo_usuario.get().strip()
        senha = entrada_nova_senha.get().strip()
        senha_confirmacao = entrada_confirmar_senha.get().strip()
        papel = papel_variavel.get()

        if not nome_usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        
        if senha != senha_confirmacao:
            messagebox.showerror("Erro", "Senhas não coincidem")
            return
        
        sucesso, mensagem = criar_novo_usuario(nome_usuario, senha, papel)
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            janela_novo_usuario.destroy()
            entrada_usuario.delete(0, tk.END)
            entrada_senha.delete(0, tk.END)
            entrada_usuario.insert(0, nome_usuario)
            entrada_senha.focus()
        else:
            messagebox.showerror("Erro", mensagem)
    
    frame_botoes = tk.Frame(frame_principal, bg=COR_FUNDO)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=15)
    
    tk.Button(
        frame_botoes, 
        text="Criar", 
        command=executar_criar_usuario, 
        width=10,
        bg=COR_SECUNDARIA,
        fg='white',
        font=(FONTE_PADRAO, 10),
        cursor="hand2"
    ).pack(side='left', padx=5)
    
    tk.Button(
        frame_botoes, 
        text="Cancelar", 
        command=janela_novo_usuario.destroy, 
        width=10,
        bg=COR_ACENTO,
        fg='white',
        font=(FONTE_PADRAO, 10),
        cursor="hand2"
    ).pack(side='left', padx=5)

def centralizar_janela(janela):
    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def cancelar_login(janela_raiz):
    global janela_login
    janela_login.destroy()
    janela_raiz.quit()

def mostrar_janela_login(janela_raiz):
    global janela_login
    janela_raiz.withdraw()
    garantir_arquivo_usuario_existe()
    
    janela_login = tk.Toplevel(janela_raiz)
    janela_login.title("Login - Pipe Puzzle Master")
    janela_login.geometry("350x250")
    janela_login.resizable(False, False)
    janela_login.configure(bg=COR_FUNDO)
    janela_login.grab_set()
    janela_login.focus_force()
    
    centralizar_janela(janela_login)
    
    frame_principal = tk.Frame(janela_login, padx=25, pady=25, bg=COR_FUNDO)
    frame_principal.pack(expand=True, fill='both')
    
    tk.Label(
        frame_principal, 
        text="Usuário:", 
        bg=COR_FUNDO, 
        fg=COR_TEXTO,
        font=(FONTE_PADRAO, 10)
    ).grid(row=0, column=0, sticky='w', pady=(0, 8))
    
    entrada_usuario = tk.Entry(
        frame_principal, 
        width=22,
        font=(FONTE_PADRAO, 10)
    )
    entrada_usuario.grid(row=0, column=1, pady=(0, 8))
    entrada_usuario.focus()
    
    tk.Label(
        frame_principal, 
        text="Senha:", 
        bg=COR_FUNDO, 
        fg=COR_TEXTO,
        font=(FONTE_PADRAO, 10)
    ).grid(row=1, column=0, sticky='w', pady=(0, 15))
    
    entrada_senha = tk.Entry(
        frame_principal, 
        width=22, 
        show='*',
        font=(FONTE_PADRAO, 10)
    )
    entrada_senha.grid(row=1, column=1, pady=(0, 15))
    
    frame_botoes = tk.Frame(frame_principal, bg=COR_FUNDO)
    frame_botoes.grid(row=2, column=0, columnspan=2, pady=10)
    
    tk.Button(
        frame_botoes, 
        text="Login", 
        command=lambda: tentar_login(entrada_usuario, entrada_senha, janela_raiz), 
        width=10,
        bg=COR_SECUNDARIA,
        fg='white',
        font=(FONTE_PADRAO, 10, 'bold'),
        cursor="hand2"
    ).pack(side='left', padx=5)
    
    tk.Button(
        frame_botoes, 
        text="Novo Usuário", 
        command=lambda: mostrar_janela_novo_usuario(entrada_usuario, entrada_senha), 
        width=12,
        bg=COR_PRIMARIA,
        fg='white',
        font=(FONTE_PADRAO, 10),
        cursor="hand2"
    ).pack(side='left', padx=5)
    
    tk.Button(
        frame_botoes, 
        text="Cancelar", 
        command=lambda: cancelar_login(janela_raiz), 
        width=10,
        bg=COR_ACENTO,
        fg='white',
        font=(FONTE_PADRAO, 10),
        cursor="hand2"
    ).pack(side='left', padx=5)
    
    entrada_senha.bind('<Return>', lambda e: tentar_login(entrada_usuario, entrada_senha, janela_raiz))

def obter_usuario_atual():
    return usuario_atual

def atualizar_usuario_atual():
    return crud.carregar_usuario(usuario_atual['usuario'])

def fazer_logout(janela_raiz, callback_logout=None):
    global usuario_atual, janela_login
    usuario_atual = None
    if callback_logout:
        callback_logout()
    
    for widget in janela_raiz.winfo_children():
        widget.destroy()
    
    mostrar_janela_login(janela_raiz)