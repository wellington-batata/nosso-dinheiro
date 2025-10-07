# nosso-dinheiro
# Nosso Dinheiro - Agente Financeiro

Este projeto é uma API para controle de despesas pessoais, utilizando FastAPI, SQLAlchemy, PostgreSQL, LangChain e OpenAI para processamento inteligente de texto e categorização automática de gastos.

## Funcionalidades
- Cadastro de despesas via texto livre (NLP)
- Extração automática de data, valor, categoria e subcategoria
- Categorização inteligente usando IA
- Listagem de despesas por usuário
- Suporte a múltiplos usuários
- Migrações de banco de dados com Alembic
- Integração com Docker e Docker Compose

## Tecnologias
- Python 3.13+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- LangChain + OpenAI
- Docker

## Como rodar localmente
1. Clone o repositório:
	```bash
	git clone https://github.com/wellington-batata/nosso-dinheiro.git
	cd nosso-dinheiro
	```
2. Crie e configure o arquivo `.env` com as variáveis:
	```env
	ENV=dev
	DATABASE_URL_LOCAL=postgresql+psycopg2://user:senha@localhost:5432/financeiro
	DATABASE_URL_DOCKER=postgresql+psycopg2://user:senha@db:5432/financeiro
	OPENAI_API_KEY=sk-...
	POSTGRES_USER=user
	POSTGRES_PASSWORD=senha
	POSTGRES_DB=financeiro
	NETWORK_NAME=meu_nome_de_rede
	DB_CONTAINER_NAME=agente-financeiro-db
	API_CONTAINER_NAME=agente-financeiro-api
	```
3. Suba o banco de dados e a API com Docker Compose:
	```bash
	docker-compose up -d --build
	```
4. Execute as migrações do banco:
	```bash
	alembic upgrade head
	```
5. Acesse a API em `http://localhost:8000/docs`

## Endpoints principais
- `POST /expenses` - Adiciona uma despesa via texto
- `GET /expenses?userId=1` - Lista despesas do usuário

## Estrutura do projeto
```
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── docker-compose.yml
├── .env
├── alembic/
│   └── ...
├── tools/
│   ├── date_now.py
│   └── categorys.py
├── prompt_template.py
└── ...
```

## Observações
- O nome da rede Docker é configurável via variável de ambiente.
- O host do banco deve ser `localhost` para comandos locais e `db` para containers.
- O projeto utiliza LangChain para integração com IA e ferramentas customizadas.

## Licença
MIT
