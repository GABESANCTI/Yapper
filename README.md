# YAPPER!

> Um mini Twitter desenvolvido com Django — atualmente trabalhando só no backend pra garantir uma estrutura bem modular :), mas logo mais React!!!

---

## Funcionalidades Atuais

- Cadastro e login de usuários devidamente autenticados
- Criação de yaps (postagens)
- Admins podem excluir yaps  
  (futuramente, usuários também poderão excluir **apenas** os próprios yaps)

---

## Estrutura do Projeto

No começo, o projeto tinha só um app: `core`. Ele fazia de tudo — desde login e autenticação até a parte dos yaps.  
Sim, é uma prática ruim :/ mas foi o jeito mais rápido de começar, já que o projeto tá sendo feito pra avaliação.

Depois de um tempo (quando eu tava implementando a `UserTimeline` e separando a `ForYou`, a timeline principal), essa estrutura começou a atrapalhar demais.  
Então dei uma pausa nas features e decidi reorganizar o código.

Separar tudo em apps (`users`, `yaps`, etc.) foi mais tenso do que eu esperava. Levei algumas horas nessa migração.  
Mas no final valeu a pena :) Agora tá bem mais fácil entender a estruturação

Ainda faltam uns ajustes no sistema de login/cadastro, mas o principal já foi.

---

## Próximos Passos

Essa nova estrutura vai segurar bem as mudanças atuais.  
Mas sei que logo mais vai rolar outra reestruturação, baseada nas novas funcionalidades que quero implementar até o final do projeto :P

---

At.te,  
**Gabe Sancti** :)
