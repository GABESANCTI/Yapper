# Yapper!  Uma pequena rede social :)

## Apresentação do Sistema e conceitos

O Yapper é uma rede social, pensada inicialemente com o objetivo de ser um blog feito para a disciplina de programação Web como trabalho avaliativo.
Desenvolvida com Django (backend) e Bootstrap (frontend). O objetivo e permitir que usuarios compartilhem posts (Yaps), interajam com curtidas e comentarios, sigam outros perfis e personalizem suas paginas.

## De onde vem o nome?
De acordo com as definições encontradas em dicionários online da lingua inglêsa, como o urban dictionary ou o wiktionary, "Yapper" é uma pessoa que fala muito. Tendo essa definição em vista e o desejo de montar uma aplicação de rede social,
optei pela adoção do nome! É um nome que é de fácil e rápida pronúncia, ainda que seja um emprestimo de outro idioma.

## Stacks
* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript, Bootstrap
* **Banco de Dados:** SQLite3
* **Controle de Versão:** Git, GitHub
* **API Externa:** icanhazdadjoke.com
## Funcionalidades da Aplicação

* **Autenticação e Perfil:** Cadastro, Login/Logout, perfil personalizavel (foto, banner, bio, nome de exibição), visualização de perfil.
* **Interação Social:** Seguir/Deixar de Seguir, Timelines (Geral, Para Voce, de Usuário), Yaps (posts) com texto e imagem.
* **Engajamento:** Curtidas em Yaps e Comentarios (AJAX), Adição de Comentários (modal), Exclusão de Yaps/Comentários.
* **Busca:** Encontre perfis por username ou nome de exibição(case insensitive).
* **Conteúdo Dinâmico:** Timeline geral com piadas aleatorias de API externa (cache 5 min pra otimizar carregamento).
* **Melhorias Visuais:** Dark Mode, Header fixo, botões flutuantes, animações sutis.
## Fluxograma de lógica de Funcionamento
```mermaid
graph TD
    A[Usuario/Navegador] -->|Requisicao| B(Projeto Django)
    B -->|Rotas URL| C{App: core}
    B -->|Rotas URL| D{App: yaps}
    C -->|Gerencia Usuario| E(core/models.py)
    D -->|Gerencia Postagens/Interacoes| H(yaps/models.py)
    D -->|Busca Piadas| K(API Externa)
    E -->|Salva/Le| P[Banco de Dados]
    H -->|Salva/Le| P
    K -->|Retorna Dados| D
    B -->|Renderiza| M[Templates/Static Files]
    M -->|Exibe| A
```
## Diagrama de Entidades e Relacionamentos
```mermaid
erDiagram
    User {
        string id PK
        string username UK
        string password
        string first_name
        string last_name
        string email
        datetime date_joined
        datetime last_login
        bool is_active
        bool is_staff
        bool is_superuser
        string display_name "NULL"
        text bio "NULL"
        string profile_picture "NULL"
        string banner_picture "NULL"
        int profile_views "DEFAULT 0"
    }

    Yap {
        string id PK
        text content
        string image "NULL"
        datetime created_at
        int views_count "DEFAULT 0"
        string user_id FK
    }

    Comment {
        string id PK
        text content
        datetime created_at
        string yap_id FK
        string user_id FK
    }

    Like {
        string id PK
        datetime created_at
        string user_id FK
        string yap_id FK "NULL"
        string comment_id FK "NULL"
    }

    User ||--o{ Yap : "cria"
    User ||--o{ Comment : "comenta"
    User ||--o{ Like : "curte"
    Yap ||--o{ Comment : "tem"
    Yap ||--o{ Like : "curtidas_de_yaps"
    Comment ||--o{ Like : "curtidas_de_comentarios"
    User }|--|{ User : "segue"

```
 
 
 # Tutorial de uso e Ativação Local

Este tutorial ira guiar voce na clonagem do repositório do Yapper, instalação das dependencias e como rodar a aplicação em seu ambiente de desenvolvimento local.
## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes programas instalados em seu sistema:

* **Python 3.x:** Recomenda-se a versaãao 3.10 ou superior. (A versão utilizada no projeto foi Python 3.13.5).
* **pip:** O gerenciador de pacotes do Python (Para conferência do pip -> "pip –version").
* **Git:** Para clonar o repositório do GitHub.

## Passos para Configuração:

1.  **Clonar o Repositório:**
    Abra seu terminal ou prompt de comando. Escolha um diretorio onde voce deseja armazenar o projeto e execute o comando Git para clonar o repositorio do Yapper:
    ```bash
    git clone https://github.com/GABESANCTI/Yapper.git
    ```

2.  **Navegar para o Diretório do Projeto:**
    Apos a clonagem, navegue para o diretorio do projeto Yapper:
    ```bash
    cd Yapper
    ```

3.  **Criar e Ativar Ambiente Virtual:**
    E uma boa prática criar um ambiente virtual para isolar as dependências do projeto das dependências globais do seu sistema.

    * Crie o ambiente virtual:
        ```bash
        python -m venv venv
        ```
    * Ative o ambiente virtual:
        * **No Windows:**
            ```bash
            venv\Scripts\activate
            ```
        * **No macOS/Linux:**
            ```bash
            source venv/bin/activate
            ```
    (Voce deve ver `(venv)` no inicio da linha de comando, indicando que o ambiente esta ativo.)

4.  **Instalar Dependências:**
    Com o ambiente virtual ativado, instale todas as bibliotecas Python necessarias listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar Banco de Dados e Migracoes:**
    O projeto utiliza SQLite3 como banco de dados. É necessário aplicar as migrações para criar as tabelas no banco de dados local.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Criar um Usuario Administrador (Superuser):**
    Para acessar o painel de administração do Django e criar usuários ou Yaps inicialmente, voce precisara de um superusuario.
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções no terminal para criar seu username, endereço de email (opcional) e senha.

7.  **Rodar o Servidor Local:**
    Agora voce pode iniciar o servidor de desenvolvimento do Django:
    ```bash
    python manage.py runserver
    ```
    O servidor estara rodando e observando por alterações nos arquivos.

8.  **Acessar a Aplicacao:**
    Abra seu navegador da web e acesse o endereço:
    ```
    Local: http://127.0.0.1:8000
    ```
    Voce sera redirecionado para a tela de login/cadastro.

    * O painel de administração do Django esta disponivel em:
        ```
        http://127.0.0.1:8000/admin/
        ```
        (Para acessar use as credenciais do superuser que voce criou.)

## Observações Importantes (para Desenvolvimento Local)

* **Banco de Dados (SQLite3):** O arquivo `db.sqlite3` é criado na raiz do projeto. Se voce deletar este arquivo, perdera todos os dados e precisara executar `python manage.py migrate` e `python manage.py createsuperuser` novamente.
* **Arquivos de Midia (Uploads):** Imagens de perfil, banners e imagens de Yaps sao salvas na pasta `media/` na raiz do projeto. Estes arquivos nao sao versionados pelo Git (devido ao `.gitignore`). Se a pasta `media/` for deletada, os uploads serao perdidos.

---
