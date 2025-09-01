import tkinter as tk
from tkinter import messagebox
import json
import Sys.Crud as crud
import Sys.Codifier as codifier

usuario_atual = None
callback_login_sucesso = None
janela_login = None

def Inicializar_Sistema_Login(raiz, callback_sucesso):
    global callback_login_sucesso
    callback_login_sucesso = callback_sucesso
    Mostrar_Janela_Login(raiz)

def Garantir_Arquivo_Usuario_Existe():
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
    usuarios = crud.Carregar_Usuarios()
    senha_codificada = codifier.Descodificar_Senha(senha)
    
    for user in usuarios:
        if user['usuario'] == usuario and user['senha'] == senha_codificada:
            return user
    return None

def Criar_Novo_Usuario(usuario, senha, papel):
    usuarios = crud.Carregar_Usuarios()
    
    if any(user['usuario'] == usuario for user in usuarios):
        return False, "Usuário já existe"
    
    novo_usuario = {
        'id': len(usuarios) + 1,
        'usuario': usuario,
        'senha': codifier.Codificar_Senha(senha),
        'papel': papel
    }
    
    usuarios.append(novo_usuario)
    crud.Salvar_Usuarios(usuarios)
    return True, "Usuário criado com sucesso"

def Tentar_Login(entrada_usuario, entrada_senha, raiz):
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
    global janela_login
    
    janela_novo = tk.Toplevel(janela_login)
    janela_novo.title("Novo Usuário")
    janela_novo.geometry("300x200")
    janela_novo.resizable(False, False)
    janela_novo.transient(janela_login)
    janela_novo.grab_set()
    
    Centralizar_Janela(janela_novo)
    
    frame = tk.Frame(janela_novo, padx=20, pady=20)
    frame.pack(expand=True, fill='both')
    
    tk.Label(frame, text="Novo Usuário:").grid(row=0, column=0, sticky='w', pady=(0, 5))
    entrada_novo_user = tk.Entry(frame, width=20)
    entrada_novo_user.grid(row=0, column=1, pady=(0, 5))
    entrada_novo_user.focus()
    
    tk.Label(frame, text="Nova Senha:").grid(row=1, column=0, sticky='w', pady=(0, 5))
    entrada_nova_senha = tk.Entry(frame, width=20, show='*')
    entrada_nova_senha.grid(row=1, column=1, pady=(0, 5))
    
    tk.Label(frame, text="Confirmar Senha:").grid(row=2, column=0, sticky='w', pady=(0, 10))
    entrada_conf_senha = tk.Entry(frame, width=20, show='*')
    entrada_conf_senha.grid(row=2, column=1, pady=(0, 10))

    papel_novo_usuario = tk.StringVar(value="user")
    radio_adm = tk.Radiobutton(frame, text="Administrador", variable=papel_novo_usuario, value="admin")
    radio_adm.grid(row=3, column=0)

    radio_user = tk.Radiobutton(frame, text="Player", variable=papel_novo_usuario, value="user")
    radio_user.grid(row=3, column=1)


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
    
    frame_botoes = tk.Frame(frame)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=5)
    
    tk.Button(frame_botoes, text="Criar", command=Executar_Criar_Usuario, width=10).pack(side='left', padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=janela_novo.destroy, width=10).pack(side='left', padx=5)

def Centralizar_Janela(janela):
    janela.update_idletasks()
    largura = janela.winfo_width()
    altura = janela.winfo_height()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def Cancelar_Login(raiz):
    global janela_login
    janela_login.destroy()
    raiz.quit()

def Mostrar_Janela_Login(raiz):
    global janela_login
    raiz.withdraw()
    Garantir_Arquivo_Usuario_Existe()
    
    janela_login = tk.Toplevel(raiz)
    janela_login.title("Login")
    janela_login.geometry("300x200")
    janela_login.resizable(False, False)
    #janela_login.transient(raiz)
    janela_login.grab_set()
    
    Centralizar_Janela(janela_login)
    
    frame = tk.Frame(janela_login, padx=20, pady=20)
    frame.pack(expand=True, fill='both')
    
    tk.Label(frame, text="Usuário:").grid(row=0, column=0, sticky='w', pady=(0, 5))
    entrada_usuario = tk.Entry(frame, width=20)
    entrada_usuario.grid(row=0, column=1, pady=(0, 5))
    entrada_usuario.focus()
    
    tk.Label(frame, text="Senha:").grid(row=1, column=0, sticky='w', pady=(0, 10))
    entrada_senha = tk.Entry(frame, width=20, show='*')
    entrada_senha.grid(row=1, column=1, pady=(0, 10))
    
    frame_botoes = tk.Frame(frame)
    frame_botoes.grid(row=2, column=0, columnspan=2, pady=10)
    
    tk.Button(frame_botoes, text="Login", command=lambda: Tentar_Login(entrada_usuario, entrada_senha, raiz), width=10).pack(side='left', padx=5)
    tk.Button(frame_botoes, text="Novo Usuário", command=lambda: Mostrar_Janela_Novo_Usuario(entrada_usuario, entrada_senha), width=10).pack(side='left', padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=lambda: Cancelar_Login(raiz), width=10).pack(side='left', padx=5)
    
    entrada_senha.bind('<Return>', lambda e: Tentar_Login(entrada_usuario, entrada_senha, raiz))

def Obter_Usuario_Atual():
    return usuario_atual

def Fazer_Logout(raiz, callback_logout=None):
    global usuario_atual, janela_login
    usuario_atual = None
    if callback_logout:
        callback_logout()
    
    for widget in raiz.winfo_children():
        widget.destroy()
    
    Mostrar_Janela_Login(raiz)