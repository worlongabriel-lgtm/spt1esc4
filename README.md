# Task Priority API

Micro-API de tarefas para uso interno de equipe, construída com FastAPI e priorização assistida por IA.

## Objetivo

O projeto entrega um MVP para cadastro, consulta, atualização e remoção de tarefas, com sugestão automática de prioridade.

A prioridade pode ser definida por heurística local ou, quando houver chave configurada, por chamada opcional a um provedor LLM. Em caso de falha externa, timeout ou ausência de chave, a API usa fallback local para manter o funcionamento sem custo obrigatório de IA.

## Stack

- Python 3.13
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest
- HTTPX
- Ambiente virtual com `venv`

## Arquitetura

O projeto segue uma separação simples por camadas:

```text
app/
  api/          # Rotas HTTP FastAPI
  models/       # Schemas Pydantic e tipos de domínio
  repository/   # Persistência em memória
  services/     # Regras de negócio e priorização
  main.py       # Instância FastAPI e registro de routers
tests/          # Testes automatizados
docs/           # Documentação técnica do MVP
```

Fluxo principal:

```text
Cliente -> API Routes -> TaskService -> TaskRepository
                         |
                         -> PriorityAdvisor -> LLM opcional ou heurística local
```

## Funcionalidades

- Health check da aplicação
- Criação de tarefas
- Listagem de tarefas
- Consulta de tarefa por ID
- Atualização de tarefa
- Remoção de tarefa
- Sugestão automática de prioridade
- Fallback local quando IA externa não estiver disponível
- Documentação interativa via Swagger/OpenAPI

## Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Criar ambiente virtual

```bash
python3 -m venv .venv
```

### 3. Ativar ambiente virtual

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

Se o sistema não tiver suporte a `venv` ou `pip`, instale antes:

```bash
sudo apt install -y python3.13-venv python3-pip
```

## Execução

Para iniciar a API em modo desenvolvimento:

```bash
uvicorn app.main:app --reload
```

API local:

```text
http://localhost:8000
```

Swagger/OpenAPI:

```text
http://localhost:8000/docs
```

## Endpoints

### Health check

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "timestamp": "2026-05-03T12:00:00+00:00"
}
```

### Criar tarefa

```http
POST /tasks
```

Exemplo de payload:

```json
{
  "title": "Revisar backlog da sprint",
  "description": "Organizar tarefas prioritárias para o time",
  "status": "pending",
  "priority": "medium"
}
```

Status esperado: `201 Created`

### Listar tarefas

```http
GET /tasks
```

Status esperado: `200 OK`

### Consultar tarefa por ID

```http
GET /tasks/{task_id}
```

Status esperado:

- `200 OK` quando a tarefa existir
- `404 Not Found` quando a tarefa não existir

### Atualizar tarefa

```http
PUT /tasks/{task_id}
```

Status esperado:

- `200 OK` quando a tarefa existir
- `404 Not Found` quando a tarefa não existir

### Remover tarefa

```http
DELETE /tasks/{task_id}
```

Status esperado:

- `204 No Content` quando a tarefa existir
- `404 Not Found` quando a tarefa não existir

## Uso de IA

O componente `PriorityAdvisor` sugere prioridade para tarefas.

Quando `OPENAI_API_KEY` não estiver configurada, a priorização usa heurística local baseada em termos encontrados no título e na descrição da tarefa.

Quando `OPENAI_API_KEY` estiver configurada, o componente tenta uma chamada opcional à API de LLM. A chamada possui timeout e fallback obrigatório para a heurística local.

Variáveis suportadas:

```env
OPENAI_API_KEY=<sua-chave>
OPENAI_MODEL=gpt-4.1-mini
```

Comportamento de fallback:

- Sem chave: usa heurística local
- Timeout: usa heurística local
- Erro de rede: usa heurística local
- Resposta inválida da LLM: usa heurística local

Prioridades suportadas:

- `low`
- `medium`
- `high`
- `urgent`

## Testes

Para executar todos os testes:

```bash
pytest -q
```

Ou usando explicitamente o Python do ambiente virtual:

```bash
.venv/bin/python -m pytest -q
```

Cobertura atual dos testes:

- `TaskService`
- `PriorityAdvisor`
- Rotas CRUD de `/tasks`
- Status HTTP `201`, `200`, `204` e `404`
- Fallback de priorização quando chamada externa falha

## Documentação técnica

Arquivos complementares:

- `docs/escopo-mvp.md`
- `docs/backlog.md`
- `docs/diagrama-componentes.md`

## Limitações

- Persistência em memória: os dados são perdidos ao reiniciar a aplicação.
- Não há autenticação ou autorização.
- Não há paginação, filtros avançados ou ordenação.
- Não há banco de dados configurado.
- Não há deploy de produção definido.
- A integração com LLM é opcional e possui fallback local.
- O objetivo atual é validar o fluxo do MVP, não operar em produção.

## Próximos passos

- Adicionar banco de dados para persistência real.
- Criar camada de configuração centralizada.
- Adicionar autenticação para uso interno.
- Implementar filtros de listagem por status, prioridade e prazo.
- Melhorar observabilidade com logs estruturados.
- Expandir testes de integração.
- Criar pipeline de CI para rodar testes automaticamente.
- Preparar configuração de deploy.

## Status do projeto

MVP em desenvolvimento, com CRUD inicial, testes automatizados e priorização assistida com fallback seguro.
