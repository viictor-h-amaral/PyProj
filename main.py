import tkinter as tk
from Sys.Login import inicializar_sistema_login, obter_usuario_atual, fazer_logout, centralizar_janela
import Sys.ExibicaoNiveis as exibicao_niveis
import Sys.ExibicaoMeusNiveis as exibicao_meus_niveis
import Sys.ExibicaoUsuarios as exibicao_usuarios

# Configurações de estilo atualizadas
FONTE_PADRAO = "Roboto"
COR_PRIMARIA = "#6366f1"
COR_SECUNDARIA = "#818cf8"
COR_ACENTO = "#f471b5"
COR_TEXTO = "#1e293b"
COR_FUNDO = "#f1f5f9"
COR_DESTAQUE = "#0ea5e9"

def main():
    janela_principal = tk.Tk()
    janela_principal.title("Pipe Puzzle Master")
    janela_principal.geometry("900x650")
    janela_principal.configure(bg=COR_FUNDO)
    centralizar_janela(janela_principal)
    
    def ao_login_sucesso(dados_usuario):
        print(f"Usuário logado: {dados_usuario['username']}")
        print(f"Papel: {dados_usuario['role']}")
        janela_principal.deiconify()
        configurar_interface_principal(janela_principal)

    inicializar_sistema_login(janela_principal, ao_login_sucesso)
    janela_principal.mainloop()

def configurar_interface_principal(janela_principal):
    for widget in janela_principal.winfo_children():
        widget.destroy()
    
    # Cabeçalho com estilo futurista
    frame_cabecalho = tk.Frame(janela_principal, bg=COR_PRIMARIA, height=70)
    frame_cabecalho.pack(fill='x')
    frame_cabecalho.pack_propagate(False)
    
    usuario_atual = obter_usuario_atual()
    rotulo_boas_vindas = tk.Label(
        frame_cabecalho, 
        text=f"Bem-vindo, {usuario_atual['username']}!",
        bg=COR_PRIMARIA, 
        fg='white', 
        font=(FONTE_PADRAO, 16, "bold")
    )
    rotulo_boas_vindas.pack(side='left', padx=25, pady=15)
    
    botao_sair = tk.Button(
        frame_cabecalho, 
        text="Sair", 
        command=lambda: fazer_logout(janela_principal, lambda: print("Logout realizado")),
        bg=COR_ACENTO, 
        fg='white', 
        font=(FONTE_PADRAO, 11, "bold"),
        relief='flat', 
        padx=20, 
        pady=8,
        cursor="hand2"
    )
    botao_sair.pack(side='right', padx=25, pady=15)
    
    frame_conteudo = tk.Frame(janela_principal, bg=COR_FUNDO)
    frame_conteudo.pack(expand=True, fill='both', padx=25, pady=25)
    
    if usuario_atual['role'] == 'admin':
        configurar_interface_administrador(frame_conteudo, janela_principal)
    else:
        configurar_interface_usuario(frame_conteudo)

def configurar_interface_administrador(frame, janela_principal):
    rotulo_titulo = tk.Label(
        frame, 
        text="Painel Administrativo", 
        font=(FONTE_PADRAO, 20, "bold"), 
        fg=COR_PRIMARIA, 
        bg=COR_FUNDO
    )
    rotulo_titulo.pack(pady=25)
    
    estilo_botao = {
        'width': 28,
        'height': 2,
        'font': (FONTE_PADRAO, 13),
        'bg': COR_SECUNDARIA,
        'fg': 'white',
        'relief': 'flat',
        'border': 0,
        'cursor': 'hand2',
        'activebackground': COR_DESTAQUE
    }
    
    tk.Button(
        frame, 
        text="Gerenciar Usuários", 
        **estilo_botao,
        command=lambda: exibicao_usuarios.mostrar_pagina_gerenciamento_usuarios(janela_principal)
    ).pack(pady=12)
    
    tk.Button(
        frame, 
        text="Acessar Níveis", 
        **estilo_botao,
        command=lambda: exibicao_niveis.mostrar_pagina_niveis(janela_principal)
    ).pack(pady=12)
    
    tk.Button(
        frame, 
        text="Meus Níveis", 
        **estilo_botao,
        command=lambda: exibicao_meus_niveis.mostrar_pagina_meus_niveis(janela_principal)
    ).pack(pady=12)
    
    tk.Button(
        frame, 
        text="Criar Nível", 
        **estilo_botao
    ).pack(pady=12)

def configurar_interface_usuario(frame):
    rotulo_titulo = tk.Label(
        frame, 
        text="Painel do Usuário", 
        font=(FONTE_PADRAO, 20, "bold"), 
        fg=COR_PRIMARIA, 
        bg=COR_FUNDO
    )
    rotulo_titulo.pack(pady=25)
    
    estilo_botao = {
        'width': 28,
        'height': 2,
        'font': (FONTE_PADRAO, 13),
        'bg': COR_SECUNDARIA,
        'fg': 'white',
        'relief': 'flat',
        'border': 0,
        'cursor': 'hand2',
        'activebackground': COR_DESTAQUE
    }
    
    tk.Button(
        frame, 
        text="Conquistas", 
        **estilo_botao
    ).pack(pady=12)
    
    tk.Button(
        frame, 
        text="Acessar Níveis", 
        **estilo_botao,
        command=lambda: exibicao_niveis.mostrar_pagina_niveis()
    ).pack(pady=12)

if __name__ == "__main__":
    main()