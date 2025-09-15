"""
Módulo principal do sistema de gerenciamento de níveis.

Este módulo contém a interface principal do sistema e gerencia a navegação
entre diferentes funcionalidades baseada no papel do usuário (admin ou usuário comum).
"""

import tkinter as tk
from Sys.Login import Inicializar_Sistema_Login, Obter_Usuario_Atual, Fazer_Logout, Centralizar_Janela, Apagar_Usuario
import Sys.LevelDisplay as LDisplay
import Sys.MyLevelsDisplay as MLDisplay
import Sys.UsersDisplay as UDisplay
import Sys.LevelCreator as LCreator
import Sys.WindowsPattern as pattern


def principal():
    """
    Função principal que inicializa a aplicação.
    
    Configura a janela principal, inicializa o sistema de login e inicia o loop principal.
    """
    raiz = tk.Tk()
    raiz.config(bg=pattern.cor_branca_paleta)
    raiz.title("Menu")
    raiz.geometry("800x600")
    Centralizar_Janela(raiz)
    pattern.Alterar_Paleta(1)
    
    def ao_login_sucesso(dados_usuario):
        """Callback executado quando o login é bem-sucedido."""
        print(f"Usuário logado: {dados_usuario['usuario']}")
        print(f"Papel: {dados_usuario['papel']}")
        raiz.deiconify()
        configurar_interface_principal(raiz)

    Inicializar_Sistema_Login(raiz, ao_login_sucesso)
    raiz.mainloop()


def configurar_interface_principal(raiz):
    """
    Configura a interface principal após login bem-sucedido.
    
    Args:
        raiz: Janela principal da aplicação
    """
    for widget in raiz.winfo_children():
        widget.destroy()
    
    frame_cabecalho = tk.Frame(raiz, height=50, bg=pattern.cor_branca_paleta)
    frame_cabecalho.pack(fill='x')
    frame_cabecalho.pack_propagate(False)
    
    usuario_atual = Obter_Usuario_Atual()
    label_boas_vindas = tk.Label(frame_cabecalho, 
                                text=f"Olá, {usuario_atual['usuario']}!",
                                font=pattern.fonte_cabecalho_22,
                                fg=pattern.cor_fonte_padrao,
                                bg=pattern.cor_branca_paleta)
    label_boas_vindas.pack(side='left', padx=20, pady=10)
    
    botao_logout = tk.Button(frame_cabecalho, 
                            text="Sair", 
                            font=pattern.fonte_cabecalho_12, 
                            fg=pattern.cor_fonte_padrao,
                            command=lambda: Fazer_Logout(raiz, lambda: print("Logout realizado")))
    botao_logout.pack(side='right', padx=20, pady=10)

    def Main_Apagar_Usuario():
        """Função para apagar o usuário atual."""
        usuario = Obter_Usuario_Atual()
        Apagar_Usuario(raiz, usuario)

    botao_exclusao_usuario = tk.Button(frame_cabecalho, 
                                        text="Apagar usuário", 
                                        font=pattern.fonte_cabecalho_11, 
                                        fg=pattern.cor_fonte_padrao, 
                                        command=lambda: Main_Apagar_Usuario())
    botao_exclusao_usuario.pack(side='right', padx=20, pady=10)
    
    frame_conteudo = tk.Frame(raiz, bg=pattern.cor_branca_paleta)
    frame_conteudo.pack(expand=True, fill='both')
    
    if usuario_atual['papel'] == 'admin':
        configurar_interface_admin(frame_conteudo, raiz)
    else:
        configurar_interface_usuario(frame_conteudo, raiz)


def configurar_interface_admin(frame, pagina):
    """
    Configura a interface para usuários administradores.
    
    Args:
        frame: Frame onde os componentes serão adicionados
        pagina: Página principal para navegação
    """
    tk.Label(frame,     
                text="Painel administrativo 👑", 
                font=pattern.fonte_cabecalho_22,
                fg=pattern.cor_fonte_padrao,
                bg=pattern.cor_branca_paleta
            ).pack(pady=20)
    
    tk.Button(frame, 
                text="Gerenciar usuários 👥",  
                width=30, height=2, 
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                command=lambda: UDisplay.Gerar_Pagina_Gerenciamento_Usuarios(pagina)
            ).pack(pady=5)

    tk.Button(frame, 
                text="Acessar níveis 🧩", 
                width=30, height=2, 
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                command=lambda: LDisplay.Gerar_Pagina_Niveis(pagina)
            ).pack(pady=5)

    tk.Button(frame, 
                text="Meus níveis 🎲", 
                width=30, height=2, 
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                command=lambda: MLDisplay.Gerar_Pagina_Meus_Niveis(pagina)
            ).pack(pady=5)

    tk.Button(frame, 
                text="Criar nível ✨", 
                width=30, height=2, 
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                command=lambda: LCreator.Gerar_Pagina_Criacao_Nivel(pagina)
            ).pack(pady=5)


def configurar_interface_usuario(frame, pagina):
    """
    Configura a interface para usuários comuns.
    
    Args:
        frame: Frame onde os componentes serão adicionados
        pagina: Página principal para navegação
    """
    tk.Label(frame, 
                text="Painel do usuário 😎", 
                font=pattern.fonte_cabecalho_22,
                fg=pattern.cor_fonte_padrao,
                bg=pattern.cor_branca_paleta
            ).pack(pady=20)
    
    tk.Button(frame, 
                text="Conquistas 🏆", 
                width=30, height=2,
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta, 
            ).pack(pady=5)

    tk.Button(frame, 
                text="Acessar níveis 🧩",
                width=30, height=2, 
                font=pattern.fonte_cabecalho_11,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta, 
                command=lambda: LDisplay.Gerar_Pagina_Niveis(pagina)
            ).pack(pady=5)


if __name__ == "__main__":
    principal()