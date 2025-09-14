import tkinter as tk
import Sys.Crud as crud
import Sys.Login as login
from tkinter import messagebox
import Sys.Codifier as codifier

controle_usuarios_exibidos = [0, 10]

def Gerar_Pagina_Gerenciamento_Usuarios(raiz):

    pagina = tk.Toplevel(raiz)
    pagina.transient(raiz)
    pagina.grab_set()
    pagina.focus_force()
    pagina.title("Usuários")
    pagina.geometry("800x500")

    login.Centralizar_Janela(pagina)

    label = tk.Label(pagina, text="Usuários", font=("Arial", 16))
    label.pack(pady=20)

    frame_usuarios = tk.Frame(pagina)
    frame_usuarios.pack(pady=20, fill='both', expand=True)

    frame_botoes_avancar_recuar = tk.Frame(pagina)
    frame_botoes_avancar_recuar.pack(pady=20, fill='both', expand=True)


    frame_usuarios_superior = tk.Frame(frame_usuarios)
    frame_usuarios_superior.pack(fill='x', pady=5, expand=True)

    frame_usuarios_inferior = tk.Frame(frame_usuarios)
    frame_usuarios_inferior.pack(fill='x', pady=5, expand=True)

    botao_recuar = tk.Button(frame_botoes_avancar_recuar, text='<', fg='white', bg='#3b68ff', 
                                        font=('Arial', 16), command=lambda: Recuar_Exibicao_Usuarios(10, frame_usuarios_superior, frame_usuarios_inferior))
    botao_recuar.pack(fill='x', pady=5, expand=True)

    botao_avancar = tk.Button(frame_botoes_avancar_recuar, text='>', fg='white', bg='#ff3b3b', 
                                        font=('Arial', 16), command=lambda: Avancar_Exibicao_Usuarios(10, frame_usuarios_superior, frame_usuarios_inferior))
    botao_avancar.pack(fill='x', pady=5, expand=True)

    Limpar_Exibir_Botoes_Usuarios(frame_usuarios_superior, frame_usuarios_inferior)

    pagina.mainloop()

def Recuar_Exibicao_Usuarios(quantidade_voltar, frame_sup, frame_inf):
    global controle_usuarios_exibidos
    if (controle_usuarios_exibidos[0] - quantidade_voltar < 0):
        return

    controle_usuarios_exibidos[0] -= quantidade_voltar
    controle_usuarios_exibidos[1] -= quantidade_voltar
    Limpar_Exibir_Botoes_Usuarios(frame_sup, frame_inf)

def Avancar_Exibicao_Usuarios(quantidade_avancar, frame_sup, frame_inf):
    global controle_usuarios_exibidos

    quantidade_usuarios_existente = len(crud.Carregar_Usuarios())

    quantidade_niveis_exibidos_nesse_momento = controle_usuarios_exibidos[1] - 1
    if (quantidade_niveis_exibidos_nesse_momento + 1 > quantidade_usuarios_existente):
        return

    controle_usuarios_exibidos[0] += quantidade_avancar
    controle_usuarios_exibidos[1] += quantidade_avancar
    Limpar_Exibir_Botoes_Usuarios(frame_sup, frame_inf)

def Limpar_Exibir_Botoes_Usuarios(frame_sup, frame_inf):
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
            nivel_button = tk.Button(frame_sup, text=usuario['usuario'], height=2, command=lambda p_user = usuario['usuario']: Exibir_Alterar_Usuario(p_user))
            nivel_button.grid(row=0, column=botoes_no_frame_superior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_superior += 1

        elif botoes_no_frame_inferior < 5:
            nivel_button = tk.Button(frame_inf, text=usuario['usuario'], height=2, command=lambda p_user = usuario['id']: Exibir_Alterar_Usuario(p_user))
            nivel_button.grid(row=0, column=botoes_no_frame_inferior, padx=10, pady=10, sticky='ew')
            botoes_no_frame_inferior += 1

        else: break

def Exibir_Alterar_Usuario(user):

    usuario = crud.Carregar_Usuario(user)
    
    janela_usuario = tk.Toplevel()
    janela_usuario.title("Alterar usuário")
    janela_usuario.geometry("300x200")
    janela_usuario.resizable(False, False)
    janela_usuario.grab_set()

    login.Centralizar_Janela(janela_usuario)

    frame = tk.Frame(janela_usuario, padx=20, pady=20)
    frame.pack(expand=True, fill='both')
    
    tk.Label(frame, text="Usuário:").grid(row=0, column=0, sticky='w', pady=(0, 5))
    entrada_user = tk.Entry(frame, width=20)
    entrada_user.insert(0, usuario['usuario'])
    entrada_user.config(state='readonly')
    entrada_user.grid(row=0, column=1, pady=(0, 5))
    
    tk.Label(frame, text="Nova senha:").grid(row=1, column=0, sticky='w', pady=(0, 5))
    entrada_senha = tk.Entry(frame, width=20, show='*')
    entrada_senha.grid(row=1, column=1, pady=(0, 5))
    entrada_senha.focus()

    def Executar_Atualizar_Usuario():
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


    tk.Label(frame, text="Confirmar nova senha:").grid(row=2, column=0, sticky='w', pady=(0, 10))
    entrada_conf_senha = tk.Entry(frame, width=20, show='*')
    entrada_conf_senha.grid(row=2, column=1, pady=(0, 10))
    entrada_conf_senha.bind('<Return>', lambda e: Executar_Atualizar_Usuario())

    papel_usuario = tk.StringVar(value=usuario['papel'])

    radio_adm = tk.Radiobutton(frame, text="Administrador", variable=papel_usuario, value="admin")
    radio_adm.config(state='disabled')
    radio_adm.grid(row=3, column=0)

    radio_user = tk.Radiobutton(frame, text="Player", variable=papel_usuario, value="user")
    radio_user.config(state='disabled')
    radio_user.grid(row=3, column=1)

    frame_botoes = tk.Frame(frame)
    frame_botoes.grid(row=4, column=0, columnspan=2, pady=5)
    
    tk.Button(frame_botoes, text="Salvar", command=Executar_Atualizar_Usuario, width=10).pack(side='left', padx=5)
    tk.Button(frame_botoes, text="Cancelar", command=janela_usuario.destroy, width=10).pack(side='left', padx=5)
    janela_usuario.mainloop()

def Atualizar_Usuario(usuario, nova_senha):
    usuarios = crud.Carregar_Usuarios()

    usuario_atual = crud.Carregar_Usuario(usuario)
    index_usuario = usuarios.index(usuario_atual) 
   
    usuario_atualizado = usuario_atual
    usuario_atualizado['senha'] = codifier.Codificar_Senha(nova_senha)

    usuarios[index_usuario] = usuario_atualizado
    crud.Salvar_Usuarios(usuarios)
    return True, "Usuário atualizado com sucesso"