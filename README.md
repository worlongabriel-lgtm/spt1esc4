# Task Priority API

MVP de uma micro-API REST para gerenciamento de tarefas com sugestão de prioridade assistida por IA. A aplicação permite criar, listar, consultar, atualizar e remover tarefas, com priorização automática baseada em heurística local ou chamada opcional a OpenAI.

## Objetivo

Entregar uma API simples, testável e organizada para controle interno de tarefas, com foco em:

- Operações CRUD completas
- Filtros por status, prioridade e data
- Validação robusta de entrada
- Separação em camadas: rotas, serviços e repositório
- Priorização assistida por IA com fallback local inteligente
- Documentação automática via Swagger/OpenAPI
- Preparação para migração para banco de dados relacional

## Status do MVP

O projeto implementa o núcleo funcional da API usando FastAPI, Pydantic e um repositório em memória. A sugestão de prioridade funciona com uma heurística local baseada em análise de palavras-chave e pode tentar usar OpenAI quando a variável OPENAI_API_KEY estiver configurada.

Observação: a persistência relacional com SQLite/PostgreSQL está prevista na arquitetura e no backlog, mas ainda não está ativa na implementação atual.

## Stack

- Python 3.13
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest
- HTTPX
- python-dotenv

## Estrutura do Projeto

```
app/
ffa85f64-5717-4562-b3fc-2c963f66afa6  api/                    # Rotas HTTP FastAPI
    task_routes.py
  models/                 # Schemas Pydantic e tipos de domínio
    task.py
  repository/             # Persistência em memória
    task_repository.py
  services/               # Regras de negócio e priorização
    task_service.py
    priority_advisor.py
  main.py                 # Instância FastAPI e registro de routers

tests/                    # Testes automatizados
  test_task_routes.py
  test_task_service.py
  test_priority_advisor.py

docs/                     # Documentação técnica
  escopo-mvp.md
  backlog.md
  diagrama-componentes.md

examples.py               # Script de exemplos em Python
examples.http             # Exemplos REST Client
examples.sh               # Exemplos com Bash/curl
EXEMPLOS.md               # Guia de exemplos
README.md                 # Documentação principal
requirements.txt
pytest.ini
.env.example
```

## Instalação

1. Clone o repositório:

```bash
git clone <URL-do-repositorio>
cd <nome-do-repositorio>
```

2. Crie um ambiente virtual:

```bash
python3 -m venv .venv
```

3. Ative o ambiente virtual:

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows (PowerShell):
```bash
.\.venv\Scripts\Activate.ps1
```

Windows (cmd):
```bash
.venv\Scripts\activate.bat
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso com Makefile

O projeto inclui um Makefile para facilitar operações comuns. Os comandos disponíveis são:

- `make install` - Cria ambiente virtual e instala dependências
- `make run` - Inicia o servidor da API em modo desenvolvimento
- `make test` - Executa os testes automatizados
- `make test-verbose` - Executa os testes com saída detalhada
- `make clean` - Remove ambiente virtual e arquivos de cache
- `make help` - Mostra ajuda com todos os comandos disponíveis

### Exemplos de uso:

```bash
# Instalação completa
make install

# Executar a API
make run

# Executar testes
make test

# Limpeza completa
make clean
```

O Makefile detecta automaticamente se existe um ambiente virtual e o utiliza quando disponível.

## Configuração

A API pode ser executada sem chave de IA. Nesse modo, a prioridade é calculada por heurística local baseada em análise de palavras-chave.

Para preparar as variáveis de ambiente, copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Windows:
```bash
copy .env.example .env
```

Para habilitar a tentativa de uso da OpenAI, configure OPENAI_API_KEY no .env:

```
OPENAI_API_KEY=sk-...sua-chave...
OPENAI_MODEL=gpt-4.1-mini
```

Se a variável não estiver definida, se houver timeout, erro externo ou resposta inválida, a aplicação usa automaticamente o fallback local. A chave é opcional para executar, testar e validar o MVP.

O arquivo .env será carregado automaticamente no startup pela biblioteca python-dotenv.

## Execução

Inicie a aplicação em modo de desenvolvimento:

```bash
uvicorn app.main:app --reload
```

URLs principais:

- API base: http://127.0.0.1:8000
- Swagger/OpenAPI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

Para validar uma instalação limpa, execute a API e acesse:

```bash
curl http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "timestamp": "2026-05-03T18:47:18.243365+00:00"
}
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /health | Verifica se a API está respondendo |
| POST | /tasks | Cria uma nova tarefa com prioridade automática |
| GET | /tasks | Lista tarefas com filtros opcionais |
| GET | /tasks/{task_id} | Busca uma tarefa por ID (UUID) |
| PUT | /tasks/{task_id} | Atualiza uma tarefa existente |
| DELETE | /tasks/{task_id} | Remove uma tarefa existente |

## Exemplos de Uso

### Criar Tarefa

```http
POST /tasks
Content-Type: application/json
```

Payload:
```json
{
  "title": "Resolver incidente crítico",
  "description": "Falha bloqueando serviço de produção",
  "status": "pending",
  "due_date": "2026-05-04T18:00:00Z"
}
```

Exemplo com curl:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Resolver incidente crítico",
    "description": "Falha bloqueando serviço de produção",
    "status": "pending",
    "due_date": "2026-05-04T18:00:00Z"
  }'
```

Resposta esperada (201 Created):

```json
{
  "id": "284d3116-8c28-4e3e-b23f-a608dbe385fa",
  "title": "Resolver incidente crítico",
  "description": "Falha bloqueando serviço de produção",
  "status": "pending",
  "priority": "urgent",
  "due_date": "2026-05-04T18:00:00Z",
  "created_at": "2026-05-03T18:47:18.261523Z",
  "updated_at": "2026-05-03T18:47:18.261523Z"
}
```

### Listar Tarefas

```http
GET /tasks
```

Parâmetros opcionais (query params):

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| status | string | Filtra por status: pending, in_progress, done, canceled |
| priority | string | Filtra por prioridade: low, medium, high, urgent |
| due_date | string | Filtra por data específica (ISO 8601) |

Exemplos:

```bash
# Listar todas as tarefas
curl http://127.0.0.1:8000/tasks

# Filtrar por status
curl "http://127.0.0.1:8000/tasks?status=pending"

# Filtrar por prioridade
curl "http://127.0.0.1:8000/tasks?priority=urgent"

# Combinar filtros
curl "http://127.0.0.1:8000/tasks?status=pending&priority=high"
```

Resposta esperada (200 OK):

```json
[
  {
    "id": "284d3116-8c28-4e3e-b23f-a608dbe385fa",
    "title": "Resolver incidente crítico",
    "description": "Falha bloqueando serviço de produção",
    "status": "pending",
    "priority": "urgent",
    "due_date": "2026-05-04T18:00:00Z",
    "created_at": "2026-05-03T18:47:18.261523Z",
    "updated_at": "2026-05-03T18:47:18.261523Z"
  }
]
```

### Buscar Tarefa por ID

```http
GET /tasks/{task_id}
```

Retorna 200 OK quando a tarefa existe ou 404 Not Found quando não é encontrada.

### Atualizar Tarefa

```http
PUT /tasks/{task_id}
Content-Type: application/json
```

Payload (todos os campos opcionais):

```json
{
  "title": "Resolver incidente crítico - URGENTE",
  "status": "in_progress",
  "priority": "urgent"
}
```

Retorna 200 OK quando a tarefa existe ou 404 Not Found quando não é encontrada.

### Remover Tarefa

```http
DELETE /tasks/{task_id}
```

Retorna 204 No Content quando a tarefa é removida ou 404 Not Found quando não é encontrada.

## Modelo de Dados

### Status Permitidos

- pending
- in_progress
- done
- canceled

### Prioridades

- low
- medium
- high
- urgent

### Campos de Entrada (POST/PUT)

| Campo | Obrigatório | Tipo | Restrições |
|-------|-------------|------|-----------|
| title | Sim | string | Min: 3, Max: 120 caracteres |
| description | Não | string | Max: 1000 caracteres |
| status | Não | enum | pending, in_progress, done, canceled |
| priority | Não | enum | low, medium, high, urgent |
| due_date | Não | datetime | ISO 8601, data futura |

### Campos de Saída (GET/POST/PUT)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único da tarefa |
| title | string | Título da tarefa |
| description | string | Descrição da tarefa |
| status | enum | Status atual da tarefa |
| priority | enum | Prioridade sugerida automaticamente |
| due_date | datetime | Prazo da tarefa (ISO 8601 UTC) |
| created_at | datetime | Data de criação (ISO 8601 UTC) |
| updated_at | datetime | Data da última atualização (ISO 8601 UTC) |

## Uso da IA

A priorização é feita pelo componente PriorityAdvisor localizado em app/services/priority_advisor.py e acionado pelo TaskService.

A integração com IA é opcional. O MVP funciona sem custo externo quando OPENAI_API_KEY não está configurada.

### Quando a IA é Acionada

1. Ao criar uma tarefa (POST /tasks)
2. Ao atualizar uma tarefa sem informar prioridade (PUT /tasks/{id})
3. A prioridade é SALVA no repositório junto com a tarefa

### Contexto Enviado para IA

A chamada envia os seguintes dados para obter sugestão de prioridade:

- title: título completo da tarefa
- description: descrição completa da tarefa
- system message: instrução para classificar em low, medium, high ou urgent

Exemplo de prompt enviado:
```
System: "Classifique a prioridade da tarefa interna. 
Responda apenas com uma destas palavras: low, medium, high, urgent."

User: "Resolver incidente crítico Falha bloqueando serviço de produção"
```

### Prioridades Retornadas pela IA

- low
- medium
- high
- urgent

### Timeout e Fallback

A chamada possui timeout de 5 segundos. Em caso de:
- Timeout
- Erro de rede
- Resposta inválida
- OPENAI_API_KEY não configurada

O sistema usa automaticamente a heurística local (ver seção abaixo).

### Heurística Local (Fallback)

Quando a IA não está disponível, o sistema analisa palavras-chave no título e descrição:

Palavras-chave para URGENT:
- urgente
- crítico / crítica
- bloqueio
- incidente

Palavras-chave para HIGH:
- importante
- prazo
- cliente
- produção

Padrão: MEDIUM (para todas as outras tarefas)

Exemplos:

```
"Resolver incidente crítico" 
  → contém "incidente" + "crítico" 
  → priority = URGENT

"Revisar código do cliente"
  → contém "cliente"
  → priority = HIGH

"Organizar reunião"
  → sem palavras-chave
  → priority = MEDIUM
```

## Testes

Execute a suíte de testes:

```bash
pytest -q
```

Ou com detalhes:

```bash
pytest -v
```

Resultado esperado em uma execução saudável:

```
22 passed in 0.45s
```

Cobertura funcional:

- Criação de tarefas com priorização automática
- Listagem com filtros (status, prioridade, data)
- Consulta por ID
- Atualização de tarefas
- Exclusão de tarefas
- Health check
- Heurística de prioridade com análise de palavras-chave
- Fallback quando chamada de IA falha, expira ou retorna valor inválido
- Tratamento de erros (validação, 404, 422)

## Exemplos de Uso

Três formas de testar a API:

### Opção 1: Swagger/OpenAPI (Recomendado)

1. Inicie a API: uvicorn app.main:app --reload
2. Acesse: http://127.0.0.1:8000/docs
3. Clique em "Try it out" nos endpoints

Também disponível em: http://127.0.0.1:8000/redoc

### Opção 2: Python Script

Execute o script de exemplos:

```bash
python examples.py
```

Demonstra:
- Health check
- Criação de 4 tarefas
- Listagem com filtros
- Consulta por ID
- Atualização de tarefa
- Deleção de tarefa
- Tratamento de erros

### Opção 3: REST Client (VS Code)

Se tiver a extensão REST Client instalada:

1. Abra examples.http
2. Clique em "Send Request" acima de cada exemplo
3. Veja a resposta ao lado

Contém 27 exemplos cobrindo todos os endpoints.

Para mais detalhes, consulte EXEMPLOS.md.

## Códigos HTTP

| Operação | Código | Significado |
|----------|--------|------------|
| GET /health | 200 | Serviço disponível |
| POST /tasks | 201 | Tarefa criada com sucesso |
| GET /tasks | 200 | Lista de tarefas retornada |
| GET /tasks/{id} | 200 | Tarefa encontrada |
| GET /tasks/{id} | 404 | Tarefa não existe |
| PUT /tasks/{id} | 200 | Tarefa atualizada |
| PUT /tasks/{id} | 404 | Tarefa não existe |
| DELETE /tasks/{id} | 204 | Tarefa deletada |
| DELETE /tasks/{id} | 404 | Tarefa não existe |
| POST /tasks (inválido) | 422 | Validação falhou |

## Arquitetura

A aplicação segue uma separação simples por camadas:

```
Cliente HTTP
    |
    v
FastAPI Routes (app/api/task_routes.py)
    |
    v
TaskService (app/services/task_service.py)
    |
    +-- TaskRepository (app/repository/task_repository.py)
    |
    +-- PriorityAdvisor (app/services/priority_advisor.py)
        |
        +-- Heurística Local
        |
        +-- OpenAI (opcional)
```

Responsabilidades:

- main.py: cria instância FastAPI, registra rotas e expõe health check
- task_routes.py: define endpoints, parâmetros HTTP, status codes
- task_service.py: concentra regras de negócio e orquestração
- priority_advisor.py: sugere prioridade com IA opcional e fallback local
- task_repository.py: armazena e manipula tarefas em memória

O repositório é mantido em memória durante a execução do processo da API. Isso facilita o MVP e os testes, mas significa que os dados são perdidos quando o servidor é parado.

## Limitações Conhecidas

- Persistência apenas em memória; dados são perdidos ao reiniciar a aplicação
- Sem autenticação, autorização ou controle de usuários
- Sem versionamento de API
- Sem paginação com envelope (apenas filtros simples)
- Sem busca textual por título
- Sem filtro de tarefas atrasadas
- Sem pipeline de CI/CD
- Sem configuração de deploy

## Próximos Passos

- Persistir tarefas em banco relacional (SQLite em desenvolvimento, PostgreSQL em produção)
- Implementar paginação com envelope de metadados
- Adicionar busca textual por título e descrição
- Adicionar filtro para tarefas com prazo vencido
- Implementar autenticação simples por API token
- Tornar configuráveis modelo de IA, timeout e parâmetros de inferência
- Adicionar logs estruturados para depuração
- Criar pipeline de lint, testes e build
- Documentar estratégia simples de deploy

## Comparação com Projeto de Referência

Este projeto foi desenvolvido seguindo princípios similares ao projeto de referência (AI Task Manager API), mas com algumas diferenças e melhorias:

| Aspecto | Projeto Atual | Projeto de Referência |
|---------|---------------|----------------------|
| Linguagem | Python 3.13 | Python 3.10+ |
| IDs | UUID (v4) | Numéricos sequenciais |
| Status | pending, in_progress, done, canceled | todo, in_progress, done |
| Campo de data | due_date | deadline |
| Nomenclatura | snake_case | camelCase |
| Prioridades | low, medium, high, urgent | low, medium, high |
| IA - Contexto | title + description | status + deadline |
| IA - Persistência | Salva no POST/PUT | Recalculada a cada GET |
| Heurística | 11 palavras-chave | 3 regras simples |
| Carregamento .env | Automático (load_dotenv) | Manual via terminal |
| Paginação | Filtros simples | limit/offset |
| Busca | Sem busca textual | Com busca por título |
| Filtro atrasadas | Sem filtro | Com filtro overdue |
| Testes | 22 testes | 30 testes |

### Melhorias Implementadas

1. UUIDs em vez de IDs sequenciais: Preparado para bancos distribuídos, sem colisões
2. Heurística mais inteligente: 11 palavras-chave em vez de 3 regras
3. Contexto completo para IA: Envia title + description em vez de apenas status + deadline
4. Persistência de prioridade: Calculada 1x no POST/PUT, não recalculada a cada GET
5. Carregamento automático de .env: python-dotenv configurado para startup
6. Status estendido: 4 status em vez de 3, incluindo canceled
7. Nomenclatura Pythônica: snake_case em vez de camelCase

### Pontos do Projeto de Referência Não Implementados

1. Paginação com envelope: Pode ser adicionado em Release 2.0
2. Busca textual: Não faz parte do escopo MVP atual
3. Filtro de tarefas atrasadas: Pode ser adicionado em Release 2.0
4. Makefile: Não necessário, Python puro é mais portável

## Comandos Úteis

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar API
uvicorn app.main:app --reload

# Rodar testes
pytest -q

# Rodar testes com detalhes
pytest -v

# Executar exemplos
python examples.py

# Executar exemplos com Bash
bash examples.sh
```

## Documentação Complementar

- docs/escopo-mvp.md: Escopo funcional do MVP
- docs/backlog.md: Backlog de releases futuras
- docs/diagrama-componentes.md: Diagrama de arquitetura
- EXEMPLOS.md: Guia completo de exemplos
- ANALISE-MELHORIAS.md: Análise de pontos de melhoria

---

Versão: 0.1.0
Data: 3 de maio de 2026
Status: MVP Completo
