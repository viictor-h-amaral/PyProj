import tkinter as tk

fonte_texto = ('Noto Sans', 10)

fonte_cabecalho_11 = ('Noto Sans', 12)
fonte_cabecalho_12 = ('Noto Sans', 12, 'bold')

fonte_cabecalho_21 = ('Noto Sans', 14)
fonte_cabecalho_22 = ('Noto Sans', 14, 'bold')
cor_fonte_padrao = '#030303'
cor_fonte_clara = '#030303'

verde = '#00e029'
amarelo = '#ffee00'
vermelho = '#f70c00'
cor_fonte_niveis = '#030303'

cor_escura_paleta = '#030303'
cor_quente_paleta = '#f70c00'   
cor_intermediaria = '#00b7ff'   
cor_fria_paleta = '#8400ff'     
cor_branca_paleta = '#ffffff'

def Alterar_Paleta(numero_paleta):
    global fonte_texto, fonte_cabecalho_11, fonte_cabecalho_12, fonte_cabecalho_21, fonte_cabecalho_22, cor_fonte_padrao, cor_fonte_clara
    global cor_fonte_niveis, verde, amarelo, vermelho
    global cor_escura_paleta, cor_quente_paleta, cor_intermediaria, cor_fria_paleta, cor_branca_paleta

    match numero_paleta:
        case 1:
            family = 'Courier'
            fonte_texto = (family, 10)

            fonte_cabecalho_11 = (family, 12)
            fonte_cabecalho_12 = (family, 12, 'bold')

            fonte_cabecalho_21 = (family, 14)
            fonte_cabecalho_22 = (family, 14, 'bold')
            cor_fonte_padrao = '#030303'
            cor_fonte_clara = '#ffffff'

            cor_fonte_niveis = '#030303'

            verde = '#00ffbb'
            amarelo = '#ffd000'
            vermelho = '#ff0055'

            cor_escura_paleta = '#030303'
            cor_quente_paleta = '#bd3737'
            cor_intermediaria = '#d4cdad'
            cor_fria_paleta = '#98c3a1'
            cor_branca_paleta = '#ffffff'

        case 2:
            family = 'Courier'

            fonte_texto = (family, 10)

            fonte_cabecalho_11 = (family, 12)
            fonte_cabecalho_12 = (family, 12, 'bold')

            fonte_cabecalho_21 = (family, 14)
            fonte_cabecalho_22 = (family, 14, 'bold')
            cor_fonte_padrao = '#030303'
            cor_fonte_clara = '#ffffff'

            cor_fonte_niveis = '#030303'

            verde = '#a3ffa8'
            amarelo = '#fcffa3'
            vermelho = '#ff8787'

            cor_escura_paleta = '#590f0c'
            cor_quente_paleta = '#ca221f'
            cor_intermediaria = '#fead26'
            cor_fria_paleta = '#b9d7a1'
            cor_branca_paleta = '#fffdc0'
        case 3:
            family = 'Courier'

            fonte_texto = (family, 10)

            fonte_cabecalho_11 = (family, 12)
            fonte_cabecalho_12 = (family, 12, 'bold')

            fonte_cabecalho_21 = (family, 14)
            fonte_cabecalho_22 = (family, 14, 'bold')
            cor_fonte_padrao = '#030303'
            cor_fonte_clara = '#ffffff'

            cor_fonte_niveis = '#030303'

            verde = '#a3ffa8'
            amarelo = '#fcffa3'
            vermelho = '#ff8787'

            cor_escura_paleta = '#2c171c'
            cor_quente_paleta = '#ff667c'
            cor_intermediaria = '#f9e5c0'
            cor_fria_paleta = '#b6d0a0'
            cor_branca_paleta = '#ffffff'