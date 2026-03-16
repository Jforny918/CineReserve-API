# 🎬 CineReserve API

API RESTful para gerenciamento de cinema desenvolvida para a **Cinépolis Natal**.

## Tecnologias

- Python 3.12
- Django 6 + Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- Docker + Docker Compose
- Swagger (drf-spectacular)
- Poetry

## Funcionalidades

- ✅ Cadastro e autenticação de usuários com JWT
- ✅ Listagem de filmes com busca e filtros
- ✅ Listagem de sessões por filme
- ✅ Mapa de assentos por sessão (Disponível / Reservado / Comprado)
- ✅ Reserva temporária de assento (10 minutos)
- ✅ Checkout e geração de ticket único
- ✅ Portal "Meus Tickets"
- ✅ Paginação em todos os endpoints de listagem
- ✅ Documentação automática via Swagger

## Como rodar o projeto

### Pré-requisitos
- Python 3.12+
- Poetry
- Docker e Docker Compose

### 1. Clone o repositório
```bash
git clone https://github.com/Jforny918/CineReserve-API.git
cd CineReserve-API
```

### 2. Instale as dependências
```bash
poetry install
```

### 3. Configure o ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=django-insecure-cinereserve-local-dev-key-mude-em-producao
DEBUG=True
DB_NAME=cinereserve
DB_USER=cinereserve_user
DB_PASSWORD=cinereserve_pass
DB_HOST=localhost
DB_PORT=5432
```

### 4. Suba o banco de dados
```bash
docker compose up -d db
```

### 5. Rode as migrations
```bash
poetry run python manage.py migrate
```

### 6. Popule o banco com dados de exemplo
```bash
poetry run python populate.py
```

### 7. Inicie o servidor
```bash
poetry run python manage.py runserver
```

## Documentação

Acesse a documentação interativa (Swagger) em:
**http://127.0.0.1:8000/api/docs/**

## 🔗 Endpoints

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/auth/register/` | Cadastro de usuário | ❌ |
| POST | `/api/auth/login/` | Login e geração de token JWT | ❌ |
| POST | `/api/auth/token/refresh/` | Refresh do token | ❌ |
| GET | `/api/auth/me/` | Dados do usuário logado | ✅ |
| GET | `/api/movies/` | Listar filmes | ❌ |
| GET | `/api/movies/{id}/` | Detalhe do filme | ❌ |
| GET | `/api/movies/{id}/sessions/` | Sessões de um filme | ❌ |
| GET | `/api/reservations/sessions/{id}/seats/` | Mapa de assentos | ❌ |
| POST | `/api/reservations/sessions/{id}/reserve/` | Reservar assento | ✅ |
| POST | `/api/reservations/sessions/{id}/checkout/` | Confirmar e gerar ticket | ✅ |
| GET | `/api/reservations/my-tickets/` | Meus tickets | ✅ |