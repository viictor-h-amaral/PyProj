# Sistema de Gerenciamento de Níveis 🎮

Este projeto é um sistema em **Python (Tkinter)** que permite criar,
visualizar, jogar e gerenciar **níveis de jogo baseados em peças**.\
Inclui também um sistema de **usuários com login, autenticação e
controle de permissões** (usuário comum e administrador).

------------------------------------------------------------------------

## 📂 Estrutura do Projeto

    Raiz
    │── main.py                # Ponto de entrada da aplicação
    │
    ├── DB/                    # Base de dados em arquivos JSON
    │   ├── Usuarios.json
    │   ├── Niveis.json
    │   ├── Estruturas.json
    │   ├── Grupos_Pecas.json
    │   └── Pecas.json
    │
    ├── Imgs/                  # Recursos visuais
    │   └── Pecas/             # Imagens de peças (referenciadas em Pecas.json)
    │
    └── Sys/                   # Módulos principais do sistema
        ├── Codifier.py        # Criptografia de senhas (SHA-256)
        ├── Crud.py            # Operações CRUD sobre JSONs (usuários, níveis, peças, etc.)
        ├── LevelCreator.py    # Interface para criação de novos níveis
        ├── LevelDisplay.py    # Exibição e interação com níveis
        ├── LevelRunner.py     # Lógica de execução e validação dos níveis
        ├── Login.py           # Sistema de login e gerenciamento de usuários
        ├── MyLevelsDisplay.py # Interface para gerenciamento dos níveis do usuário logado
        ├── UsersDisplay.py    # Interface administrativa para gerenciar usuários
        └── WindowsPattern.py  # Definições de cores, fontes e estilos visuais

------------------------------------------------------------------------

## ⚙️ Funcionalidades

-   **Sistema de Login**
    -   Usuário padrão `admin/admin` é criado automaticamente.
    -   Suporte a criação e exclusão de contas.
    -   Controle de papéis: **admin** 👑 e **usuário comum**.
-   **Gerenciamento de Usuários (admin)**
    -   Listagem paginada (10 por vez).
    -   Alteração de senhas.
    -   Exclusão de contas.
-   **Sistema de conquistas**
    -   Há cinco conquistas padrão no jogo.
    -   Apenas usuários comuns possuem conquistas.
-   **Níveis**
    -   Criar níveis customizados (dimensões, peças, validação).
    -   Visualizar níveis concluídos e incompletos.
    -   Jogar níveis interativos.
    -   Apagar níveis próprios.
-   **Interface**
    -   Construída em **Tkinter**.
    -   Paleta de cores e fontes configurável em `WindowsPattern.py`.

------------------------------------------------------------------------

## ▶️ Como Executar

1.  Certifique-se de ter o **Python 3.10+** instalado.

2.  Clone ou baixe este repositório.

3.  Instale as dependências necessárias:

    ``` bash
    pip install pillow
    ```

    (usado para manipulação de imagens).

4.  Execute o sistema:

    ``` bash
    python main.py
    ```

------------------------------------------------------------------------

## 🔑 Usuário Padrão

-   **Login:** `admin`\
-   **Senha:** `admin`

Esse usuário tem papel de **administrador** e pode gerenciar outros
usuários.

------------------------------------------------------------------------

## 🗂️ Estrutura dos Arquivos JSON

-   **Usuarios.json** → lista de usuários com atributos (`id`,
    `usuario`, `senha`, `papel`, `niveis_concluidos`).
-   **Niveis.json** → níveis criados, incluindo nome, dificuldade,
    criador e estrutura.
-   **Estruturas.json** → definição da matriz de peças de cada nível.
-   **Grupos_Pecas.json** → organização das peças em grupos (para
    rotação/substituição).
-   **Pecas.json** → catálogo das peças disponíveis e suas imagens em
    `/Imgs/Pecas`.

------------------------------------------------------------------------

## 🚀 Possíveis Extensões Futuras

-   Exportação e importação de níveis.
-   Editor visual de grupos de peças.

------------------------------------------------------------------------

## 👨‍💻 Autoria

Projeto desenvolvido em Python com Tkinter, focado em **aprendizado,
lógica de jogos e manipulação de interfaces gráficas e desenvolvimento
com IA**.

------------------------------------------------------------------------
