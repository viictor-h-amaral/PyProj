import tkinter as tk
from Sys.Login import Inicializar_Sistema_Login, Obter_Usuario_Atual, Fazer_Logout, Centralizar_Janela
import Sys.LevelDisplay as LDisplay
import Sys.UsersDisplay as UDisplay
import Sys.Crud as crud 

def principal():
    raiz = tk.Tk()
    raiz.title("Sistema Principal")
    raiz.geometry("800x600")
    Centralizar_Janela(raiz)
    
    def ao_login_sucesso(dados_usuario):
        print(f"Usuário logado: {dados_usuario['usuario']}")
        print(f"Papel: {dados_usuario['papel']}")
        raiz.deiconify()
        configurar_interface_principal(raiz)

    Inicializar_Sistema_Login(raiz, ao_login_sucesso)
    raiz.mainloop()

def configurar_interface_principal(raiz):
    for widget in raiz.winfo_children():
        widget.destroy()
    
    frame_cabecalho = tk.Frame(raiz, bg='lightgray', height=50)
    frame_cabecalho.pack(fill='x')
    frame_cabecalho.pack_propagate(False)
    
    usuario_atual = Obter_Usuario_Atual()
    label_boas_vindas = tk.Label(frame_cabecalho, 
                               text=f"Olá, {usuario_atual['usuario']}!",
                               bg='lightgray', font=("Arial", 14))
    label_boas_vindas.pack(side='left', padx=20, pady=10)
    
    botao_logout = tk.Button(frame_cabecalho, text="Sair", 
                          command=lambda: Fazer_Logout(raiz, lambda: print("Logout realizado")))
    botao_logout.pack(side='right', padx=20, pady=10)
    
    frame_conteudo = tk.Frame(raiz)
    frame_conteudo.pack(expand=True, fill='both', padx=20, pady=20)
    
    if usuario_atual['papel'] == 'admin':
        configurar_interface_admin(frame_conteudo)
    else:
        configurar_interface_usuario(frame_conteudo)

def configurar_interface_admin(frame):

    label = tk.Label(frame, text="Painel Administrativo", font=("Arial", 16))
    label.pack(pady=20)
    
    tk.Button(frame, text="Gerenciar Usuários", width=20, height=2, command=lambda: UDisplay.Gerar_Pagina_Gerenciamento_Usuarios()).pack(pady=5)
    tk.Button(frame, text="Acessar Níveis", width=20, height=2, command=lambda: LDisplay.Gerar_Pagina_Niveis()).pack(pady=5)
    tk.Button(frame, text="Meus níveis", width=20, height=2).pack(pady=5)
    tk.Button(frame, text="Criar nível", width=20, height=2).pack(pady=5)

def configurar_interface_usuario(frame):
    label = tk.Label(frame, text="Painel do Usuário", font=("Arial", 16))
    label.pack(pady=20)
    
    tk.Button(frame, text="Conquistas", width=20, height=2).pack(pady=5)
    tk.Button(frame, text="Acessar níveis", width=20, height=2, command=lambda: LDisplay.Gerar_Pagina_Niveis()).pack(pady=5)


if __name__ == "__main__":
    principal()