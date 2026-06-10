# Bem-vindo ao LUMOS

Esse é o manual de contribuição do nosso projeto. Nesse documento vamos falar sobre:

- Pré-requisitos
- Instalação das dependências
- Configuração do ambiente
- Criação e ativação do ambiente virtual
- Comandos para rodar o projeto
- Comandos para rodar os testes
- Orientações para commits e contribuição

---

## Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads/)
- **pip**: Gerenciador de pacotes Python (já vem instalado com o Python)

---

## Instalação das dependências

Após clonar o repositório e ativar o ambiente virtual (veja as seções abaixo), instale as dependências do projeto com:

```bash
pip install -r requirements.txt
```

---

## Configuração do ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/brncluis/projeto_arca_ensina.git
cd lumos
```

### 2. Configure o banco de dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. (Opcional) Crie um superusuário

Para acessar o painel de administração do Django:

```bash
python manage.py createsuperuser
```

---

## Criação e ativação do ambiente virtual

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Comandos para rodar o projeto

Com o ambiente virtual ativado e as dependências instaladas, rode o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse o projeto em `http://localhost:8000` no seu navegador.
Obs: Link vem no terminal, segure CTRL e clique com o botão direito.

---

## Comandos para rodar os testes

Rodar os testes é obrigatório antes de abrir um Pull Request. Use os comandos abaixo:

### Todos os testes

```bash
python manage.py test
```

### Testes de um app específico

```bash
python manage.py test nome_do_app
```

### Checklist antes de abrir o PR

- [ ] Todos os testes passam sem erros
- [ ] Adicionei testes para novas funcionalidades
- [ ] Não quebrei testes existentes
- [ ] O projeto roda corretamente no servidor local

---

## Orientações para commits e contribuição

1. Crie uma branch a partir da `main` com um nome descritivo:

```bash
git checkout -b nome-da-funcionalidade
```

2. Faça suas alterações e teste localmente.

3. Faça o commit seguindo o padrão abaixo.

4. Envie a branch para o repositório remoto:

```bash
git push origin nome-da-funcionalidade
```

### Regras gerais

- Nunca faça push direto na branch `main`.
- Sempre abra um Pull Request e descreva o que foi feito e por quê.
- Comunique-se com a equipe antes de grandes alterações.
- Mantenha o código documentado: atualize o README e adicione comentários quando necessário.
- Siga os padrões de código já existentes no projeto.

---

## Obrigado por querer contribuir!

Esse foi o manual de contribuição do LUMOS. Obrigado por querer fazer parte desse projeto. Siga as orientações acima, comunique-se com a equipe e boas contribuições!
