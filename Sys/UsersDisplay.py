"""
Módulo de Gerenciamento de Usuários (Tkinter)
---------------------------------------------

Este módulo fornece a interface gráfica para o gerenciamento de usuários do sistema,
permitindo:

- Listagem paginada de usuários (10 por vez).
- Avançar e recuar entre páginas de usuários.
- Seleção de um usuário para alteração de senha.
- Atualização da senha de um usuário no banco de dados.

Dependências:
- tkinter: construção da interface gráfica.
- Sys.Crud: operações CRUD de usuários (carregar, salvar, atualizar).
- Sys.Login: funções auxiliares de login (ex: centralizar janelas).
- Sys.Codifier: responsável por codificar senhas.
- Sys.WindowsPattern: contém padrões de fonte e cores para padronizar a interface.

Variáveis globais:
- controle_usuarios_exibidos: define o intervalo [início, fim] de usuários exibidos na tela.
"""

import tkinter as tk
import Sys.Crud as crud
import Sys.Login as login
from tkinter import messagebox
import Sys.Codifier as codifier
import Sys.WindowsPattern as pattern

# Intervalo inicial de exibição de usuários (primeira "página" de 10 registros)
controle_usuarios_exibidos = [0, 10]


def Gerar_Pagina_Gerenciamento_Usuarios(raiz):
    """
    Cria e exibe a janela principal de gerenciamento de usuários.

    Args:
        raiz (tk.Tk): janela principal da aplicação.

    Recursos da janela:
    - Exibe botões com os usuários cadastrados (10 por página).
    - Botões "<" e ">" permitem navegar entre páginas de usuários.
    - Cada botão de usuário abre a tela de alteração de senha.
    """
    pagina = tk.Toplevel(raiz)
    pagina.transient(raiz)
    pagina.grab_set()
    pagina.focus_force()
    pagina.title("Usuários")
    pagina.geometry("800x500")

    login.Centralizar_Janela(pagina)

    label = tk.Label(   pagina, 
                        text="Usuários", 
                        font=pattern.fonte_cabecalho_22,
                        fg=pattern.cor_fonte_padrao)
    label.pack(pady=20)

    frame_usuarios = tk.Frame(pagina)
    frame_usuarios.pack(pady=20, fill='both', expand=True)

    frame_botoes_avancar_recuar = tk.Frame(pagina)
    frame_botoes_avancar_recuar.pack(pady=20, fill='both', expand=True)

    frame_usuarios_superior = tk.Frame(frame_usuarios)
    frame_usuarios_superior.pack(fill='x', pady=5, expand=True)

    frame_usuarios_inferior = tk.Frame(frame_usuarios)
    frame_usuarios_inferior.pack(fill='x', pady=5, expand=True)

    botao_recuar = tk.Button(frame_botoes_avancar_recuar, text='<', fg=pattern.cor_branca_paleta, bg='#3b68ff', 
                                        font=pattern.fonte_cabecalho_11, command=lambda: Recuar_Exibicao_Usuarios(10, frame_usuarios_superior, frame_usuarios_inferior))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg=pattern.cor_branca_paleta, bg='#ff3b3b', 
                                        font=pattern.fonte_cabecalho_11, command=lambda: Avancar_Exibicao_Usuarios(10, frame_usuarios_superior, frame_usuarios_inferior))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Usuarios(frame_usuarios_superior, frame_usuarios_inferior)

    pagina.mainloop()


def Recuar_Exibicao_Usuarios(quantidade_voltar, frame_sup, frame_inf):
    """
    Move a exibição de usuários para trás (página anterior).

    Args:
        quantidade_voltar (int): quantidade de usuários a recuar (normalmente 10).
        frame_sup (tk.Frame): frame superior onde os botões de usuários são exibidos.
        frame_inf (tk.Frame): frame inferior onde os botões de usuários são exibidos.
    """
    global controle_usuarios_exibidos
    if (controle_usuarios_exibidos[0] - quantidade_voltar < 0):
        return

    controle_usuarios_exibidos[0] -= quantidade_voltar
    controle_usuarios_exibidos[1] -= quantidade_voltar
    Limpar_Exibir_Botoes_Usuarios(frame_sup, frame_inf)


def Avancar_Exibicao_Usuarios(quantidade_avancar, frame_sup, frame_inf):
    """
    Move a exibição de usuários para frente (próxima página).

    Args:
        quantidade_avancar (int): quantidade de usuários a avançar (normalmente 10).
        frame_sup (tk.Frame): frame superior onde os botões de usuários são exibidos.
        frame_inf (tk.Frame): frame inferior onde os botões de usuários são exibidos.
    """
    global controle_usuarios_exibidos

    quantidade_usuarios_existente = len(crud.Carregar_Usuarios())

    quantidade_niveis_exibidos_nesse_momento = controle_usuarios_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_usuarios_existente):
        return

    controle_usuarios_exibidos[0] += quantidade_avancar
    controle_usuarios_exibidos[1] += quantidade_avancar
    Limpar_Exibir_Botoes_Usuarios(frame_sup, frame_inf)


def Limpar_Exibir_Botoes_Usuarios(frame_sup, frame_inf):
    """
    Limpa os frames e exibe os botões correspondentes aos usuários
    no intervalo definido por `controle_usuarios_exibidos`.

    Args:
        frame_sup (tk.Frame): frame superior da janela de usuários.
        frame_inf (tk.Frame): frame inferior da janela de usuários.

    Observações:
    - Exibe até 10 usuários por página, distribuídos em dois frames (5 em cima, 5 embaixo).
    - Cada botão é associado ao evento de abrir a tela de alteração de senha.
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

    usuarios = crud.Carregar_Usuarios()[controle_usuarios_exibidos[0]:controle_usuarios_exibidos[1]]

    for usuario in usuarios:

        if botoes_no_frame_superior < 5:
            nivel_button = tk.Button(   frame_sup, 
                                        text=usuario['usuario'],
                                        font=pattern.fonte_cabecalho_12,
                                        fg=pattern.cor_fonte_padrao,
                                        height=2, 
                                        command=lambda p_user = usuario['usuario']: Exibir_Alterar_Usuario(p_user))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(   frame_inf, 
                                        text=usuario['usuario'],
                                        font=pattern.fonte_cabecalho_12,
                                        fg=pattern.cor_fonte_padrao,
                                        height=2, 
                                        command=lambda p_user = usuario['id']: Exibir_Alterar_Usuario(p_user))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: break


def Exibir_Alterar_Usuario(user):
    """
    Abre uma janela para alterar a senha de um usuário específico.

    Args:
        user (str|int): nome ou ID do usuário a ser editado.

    Recursos da janela:
    - Campo somente leitura com o nome do usuário.
    - Campos para digitar e confirmar a nova senha.
    - Botões "Salvar" e "Cancelar".
    - Validações:
        * Campos obrigatórios.
        * Senha e confirmação devem coincidir.
    - Chama `Atualizar_Usuario` para aplicar a alteração.
    """
    usuario = crud.Carregar_Usuario(user)
    
    janela_usuario = tk.Toplevel()
    janela_usuario.title("Alterar usuário")
    janela_usuario.geometry("450x200")
    janela_usuario.resizable(False, False)
    janela_usuario.grab_set()

    login.Centralizar_Janela(janela_usuario)

    frame = tk.Frame(janela_usuario, padx=20, pady=20)
    frame.pack(expand=True, fill='both')
    
    tk.Label(   frame, 
                text="Usuário: ", 
                font=pattern.fonte_cabecalho_12, 
                fg=pattern.cor_fonte_padrao
            ).grid(row=0, column=0, sticky='w', pady=(0, 5))

    entrada_user = tk.Entry(    frame, 
                                width=20, 
                                font=pattern.fonte_texto, 
                                fg=pattern.cor_fonte_padrao)
    entrada_user.insert(0, usuario['usuario'])
    entrada_user.config(state='readonly')
    entrada_user.grid(row=0, column=1, pady=(0, 5))
    
    tk.Label(   frame, 
                text="Nova senha:",
                font=pattern.fonte_cabecalho_12, 
                fg=pattern.cor_fonte_padrao
            ).grid(row=1, column=0, sticky='w', pady=(0, 5))

    entrada_senha = tk.Entry(   frame, 
                                width=20, 
                                show='*',
                                font=pattern.fonte_texto, 
                                fg=pattern.cor_fonte_padrao)
    entrada_senha.grid(row=1, column=1, pady=(0, 5))
    entrada_senha.focus()

    def Executar_Atualizar_Usuario():
        """Valida e executa a atualização da senha do usuário."""
        senha = entrada_senha.get().strip()
        confirmar_senha = entrada_conf_senha.get().strip()

        if not senha or not confirmar_senha:
            messagebox.showerror("Erro", "Todos os campos devem estar preenchidos")
            return
                
        if senha != confirmar_senha:
            messagebox.showerror("Erro", "Senhas não coincidem")
            return

        sucesso, mensagem = Atualizar_Usuario(usuario['usuario'], senha)
        if sucesso:
            messagebox.showinfo("Sucesso ao atualizar o usuário!", mensagem)
            janela_usuario.destroy()
        else:
            messagebox.showerror("Erro ao atualizar usuário!", mensagem)

    tk.Label(   frame, 
                text="Confirmar nova senha:", 
                font=pattern.fonte_cabecalho_12, 
                fg=pattern.cor_fonte_padrao
            ).grid(row=2, column=0, sticky='w', pady=(0, 10))

    entrada_conf_senha = tk.Entry(  frame, 
                                    width=20, 
                                    show='*', 
                                    font=pattern.fonte_texto, 
                                    fg=pattern.cor_fonte_padrao)
    entrada_conf_senha.grid(row=2, column=1, pady=(0, 10))
    entrada_conf_senha.bind('<Return>', lambda e: Executar_Atualizar_Usuario())

    papel_usuario = tk.StringVar(value=usuario['papel'])

    radio_adm = tk.Radiobutton( frame, 
                                text="Administrador",
                                font=pattern.fonte_texto,
                                fg=pattern.cor_fonte_padrao, 
                                variable=papel_usuario, 
                                value="admin")
    radio_adm.config(state='disabled')
    radio_adm.grid(row=3, column=0)

    radio_user = tk.Radiobutton(frame, 
                                text="Player", 
                                font=pattern.fonte_texto,
                                fg=pattern.cor_fonte_padrao, 
                                variable=papel_usuario, 
                                value="user")
    radio_user.config(state='disabled')
    radio_user.grid(row=3, column=1)

    frame_botoes = tk.Frame(frame)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=5)
    
    tk.Button(  frame_botoes, 
                text="Salvar",
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_padrao,
                bg=pattern.cor_fria_paleta,
                command=Executar_Atualizar_Usuario, 
                width=10
            ).pack(side='right', padx=5)

    tk.Button(  frame_botoes, 
                text="Cancelar",
                font=pattern.fonte_cabecalho_12,
                fg=pattern.cor_fonte_clara,
                bg=pattern.cor_escura_paleta,
                command=janela_usuario.destroy, 
                width=10
            ).pack(side='left', padx=5)

    janela_usuario.mainloop()


def Atualizar_Usuario(usuario, nova_senha):
    """
    Atualiza a senha de um usuário no banco de dados.

    Args:
        usuario (str): nome do usuário a ser atualizado.
        nova_senha (str): nova senha em texto plano.

    Returns:
        tuple: (sucesso: bool, mensagem: str)
            - True, "Usuário atualizado com sucesso" em caso de êxito.
            - False, mensagem de erro em caso de falha.

    Funcionamento:
    - Carrega todos os usuários do banco.
    - Localiza o usuário a ser atualizado.
    - Codifica a nova senha usando `codifier.Codificar_Senha`.
    - Salva a lista atualizada de usuários.
    """
    usuarios = crud.Carregar_Usuarios()

    usuario_atual = crud.Carregar_Usuario(usuario)
    index_usuario = usuarios.index(usuario_atual) 
   
    usuario_atualizado = usuario_atual
    usuario_atualizado['senha'] = codifier.Codificar_Senha(nova_senha)

    usuarios[index_usuario] = usuario_atualizado
    crud.Salvar_Usuarios(usuarios)
    return True, "Usuário atualizado com sucesso"
