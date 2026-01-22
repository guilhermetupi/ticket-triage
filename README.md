# Ticket Triage

Servico de triagem de tickets com IA. A API recebe tickets, cria jobs de triagem e processa em lote usando LLM. O estado fica no Postgres e cada execucao gera logs estruturados e registros de auditoria.

## Requisitos

- Python >= 3.13
- Postgres 17+

## Principais recursos

- API REST com FastAPI para criar tickets (unitario e em lote)
- Pipeline de triagem com jobs, batches e logs
- Integracao com LLM via Ollama (configuravel por env)
- Prompts versionados no banco (tabela prompts)
- Arquitetura em camadas com entidades e regras de dominio

## Arquitetura

- presentation: FastAPI routers, controllers, DTOs e handlers de erro
- application: use cases e commands (API publica execute(command))
- domain: entidades imutaveis, enums, excecoes e gateways
- infrastructure: SQLAlchemy, repositorios, mappers, DI e client LLM

## Estados e regras

- Ticket: PENDING -> ON_TRIAGE -> COMPLETED/FAILED
- TriageJob: PENDING/FAILED -> RUNNING -> DONE/FAILED (max 3 attempts)
- Batch: RUNNING -> DONE

## Fluxo de triagem

1. POST /tickets cria Ticket (PENDING) e TriageJob (PENDING).
2. POST /triage-jobs/batch cria um batch com jobs pendentes (PENDING ou FAILED, attempts < 3).
3. O background task processa itens em paralelo:
   - marca o job/item como RUNNING
   - carrega ticket e prompt ativo
   - chama o LLM e valida JSON de saida
   - atualiza status do ticket e do job
   - grava TriageJobLog

## Endpoints

### POST /tickets

Request:

```json
{
  "title": "Checkout returns 500",
  "description": "Client reports error when paying and cannot finish checkout.",
  "external_id": "ABC-123",
  "owner_id": "00000000-0000-0000-0000-000000000000"
}
```

Response (201):

```json
{
  "id": "4f1d2a52-60f2-4a0f-9a7c-fb27f2c94d2b",
  "title": "Checkout returns 500",
  "description": "Client reports error when paying and cannot finish checkout.",
  "external_id": "ABC-123",
  "owner_id": "00000000-0000-0000-0000-000000000000",
  "triage_status": "PENDING",
  "created_at": "2026-01-21T17:15:23.000000+00:00",
  "updated_at": "2026-01-21T17:15:23.000000+00:00"
}
```

### POST /tickets/batch

Request: lista de tickets (CreateTicketRequest).

Response (207):

```json
{
  "results": [
    {
      "status": "CREATED",
      "ticket_id": "4f1d2a52-60f2-4a0f-9a7c-fb27f2c94d2b",
      "external_id": "ABC-123",
      "owner_id": "00000000-0000-0000-0000-000000000000"
    }
  ]
}
```

### POST /triage-jobs/batch

Response (202):

```json
{
  "status": "QUEUED",
  "batch": {
    "id": "7a54bff2-6a1c-48b6-b777-7d1bbf5c8db9",
    "total_items": 10
  }
}
```

Response quando nao ha jobs:

```json
{
  "status": "EMPTY",
  "batch": null,
  "total_items": 0
}
```

## Modelo de dados (principais tabelas)

- owners
- tickets
- triage_jobs
- triage_job_batches
- triage_job_batch_items
- prompts
- triage_job_logs

## Configuracao

Variaveis de ambiente:

- DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
- DATABASE_URL (usado pelo SQLAlchemy)
- LLM_BASE_URL (endpoint POST esperado pelo OllamaClient)
- LLM_MODEL
- LOG_LEVEL (opcional)

Exemplo `.env`:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=ticket_triage
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/ticket_triage
LLM_BASE_URL=http://localhost:11434/api/chat
LLM_MODEL=llama3
LOG_LEVEL=INFO
```

## Rodando local

### 1) Banco

```bash
docker compose up -d
```

### 2) Dependencias

Com uv:

```bash
uv venv
source .venv/bin/activate
uv sync
```

Ou com pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3) Migracoes

```bash
alembic upgrade head
```

### 4) API

```bash
uvicorn app.main:app --reload
```

## Observabilidade

Logs estruturados em JSON via `app.infrastructure.logging`. Ajuste o nivel com `LOG_LEVEL`.
