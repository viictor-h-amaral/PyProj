import tkinter as tk
from Sys.Login import Centralizar_Janela, Obter_Usuario_Atual
import Sys.WindowsPattern as pattern
import Sys.Crud as crud

def Gerar_Pagina_Conquistas(raiz):
    janela_conquistas = tk.Toplevel(raiz)
    janela_conquistas.transient(raiz)
    janela_conquistas.grab_set()
    janela_conquistas.focus_force()

    def ao_fechar_pagina_niveis():
        """Fecha a página de conquistas e libera o controle da janela principal."""
        janela_conquistas.destroy()
        raiz.focus_force()
        raiz.grab_release()  # Libera o grab da janela principal
    
    janela_conquistas.protocol("WM_DELETE_WINDOW", ao_fechar_pagina_niveis)

    janela_conquistas.title("Minhas conquistas")
    janela_conquistas.geometry("1100x250")

    Centralizar_Janela(janela_conquistas)

    label = tk.Label(   janela_conquistas, 
                        text="Minhas conquistas", 
                        font=pattern.fonte_cabecalho_22,
                        fg=pattern.cor_fonte_padrao)
    label.pack(pady=20)

    frame_conquistas = tk.Frame(janela_conquistas)
    frame_conquistas.pack(pady=20, padx=10, fill='both', expand=True)

    for i in range(4):
        frame_conquistas.columnconfigure(i, weight=1)

    conquistas = crud.Buscar_Conquistas()
    conquistas_usuario = crud.Retornar_Conquistas_Usuario(Obter_Usuario_Atual())

    ultima_coluna_ocupada = 0
    for conquista in conquistas:
        conquista_frame = tk.Frame(frame_conquistas, bg=pattern.cor_branca_paleta)
        conquista_frame.grid(row=0, column=ultima_coluna_ocupada)

        lbl_descricao = tk.Label(conquista_frame, text=conquista['descricao'], 
                font=pattern.fonte_cabecalho_21,
                fg=pattern.vermelho,
                bg=pattern.cor_branca_paleta
            )
        lbl_descricao.grid(row=0, column=0)

        lbl_legenda = tk.Label(conquista_frame, text=conquista['legenda'], 
                font=pattern.fonte_texto,
                fg=pattern.cor_fonte_padrao,
                bg=pattern.cor_branca_paleta
            )
        lbl_legenda.grid(row=1, column=0)

        if conquista not in conquistas_usuario:
            lbl_descricao.config(state='disabled')
            lbl_legenda.config(state='disabled')

        ultima_coluna_ocupada += 1

    janela_conquistas.mainloop()