# Exemplos de Uso da Task Priority API

Este documento apresenta as diferentes formas de testar e usar a Task Priority API.

## Início rápido

### 1. Iniciar a API

```bash
cd /home/worlon/git-repo
source .venv/bin/activate
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

## Formas de Testar

### Opção 1: Swagger/OpenAPI (Interface Web)

A forma mais rápida de começar - nenhuma configuração necessária!

1. Com a API rodando, acesse: **http://localhost:8000/docs**
2. Clique em "Try it out" nos endpoints
3. Preencha os campos e execute

Também disponível em: **http://localhost:8000/redoc** (documentação alternativa)

### Opção 2: Python Script Interativo

Execute o script `examples.py` para ver a API em ação:

```bash
python examples.py
```

**O que faz:**
- Health check
- Cria 4 tarefas com diferentes prioridades
- Lista todas as tarefas
- Filtra por status e prioridade
- Consulta tarefa específica
- Atualiza e deleta tarefas
- Demonstra tratamento de erros

**Saída esperada:** 22 passos com exemplos práticos

### Opção 3: REST Client (VS Code)

Se tiver a extensão **REST Client** instalada:

1. Abra o arquivo `examples.http`
2. Clique em **Send Request** acima de cada exemplo
3. Veja a resposta no painel ao lado

**27 exemplos cobrindo:**
- Todos os endpoints
- Filtros e query params
- Criação, atualização e deleção
- Tratamento de erros

### Opção 4: Curl (Linha de Comando)

Execute o script `examples.sh`:

```bash
bash examples.sh
```

**O que faz:**
- Usa `curl` para demonstrar requisições HTTP
- Formata output com `jq` (se instalado)
- Exemplos de GET, POST, PUT, DELETE
- Casos de teste e erros

**Requer:**
- `curl` (geralmente pré-instalado)
- `jq` (opcional, para melhor formatação): `sudo apt install jq`

### Opção 5: Ferramentas Gráficas

#### Insomnia

1. Baixe em https://insomnia.rest
2. Create a new request
3. Copie as requisições do arquivo `examples.http`

#### Postman

1. Baixe em https://postman.com
2. New → HTTP Request
3. Copie os exemplos de `examples.http`

#### Thunder Client (VS Code)

Similar a REST Client, com interface gráfica integrada.

## Exemplos Rápidos por Curl

### Health Check
```bash
curl -s http://localhost:8000/health | jq
```

### Criar uma tarefa
```bash
curl -s -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Minha primeira tarefa",
    "description": "Descrição opcional",
    "due_date": "2026-05-10T00:00:00Z"
  }' | jq
```

### Listar tarefas
```bash
curl -s http://localhost:8000/tasks | jq '.[] | {id, title, priority, status}'
```

### Filtrar por prioridade
```bash
curl -s "http://localhost:8000/tasks?priority=urgent" | jq
```

### Filtrar por status
```bash
curl -s "http://localhost:8000/tasks?status=in_progress" | jq
```

### Consultar tarefa por ID (substitua o UUID)
```bash
curl -s http://localhost:8000/tasks/284d3116-8c28-4e3e-b23f-a608dbe385fa | jq
```

### Atualizar tarefa
```bash
curl -s -X PUT http://localhost:8000/tasks/284d3116-8c28-4e3e-b23f-a608dbe385fa \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "priority": "high"
  }' | jq
```

### Deletar tarefa
```bash
curl -i -X DELETE http://localhost:8000/tasks/284d3116-8c28-4e3e-b23f-a608dbe385fa
```

## Campos de Tarefa

### Criar/Atualizar (Input)

| Campo | Tipo | Obrigatório | Valores | Exemplo |
|-------|------|-------------|--------|---------|
| `title` | string | ✓ | min: 3, max: 120 | "Resolver bug crítico" |
| `description` | string | ✗ | max: 1000 | "Falha no login" |
| `status` | enum | ✗ | pending, in_progress, done, canceled | "pending" |
| `priority` | enum | ✗ | low, medium, high, urgent | "high" |
| `due_date` | datetime | ✗ | ISO 8601, futuro | "2026-05-10T18:00:00Z" |

### Consultar (Output)

Além dos campos acima:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `created_at` | datetime | Data de criação (ISO 8601 UTC) |
| `updated_at` | datetime | Data da última atualização |

## Priorização com IA (Opcional)

A API pode usar IA para sugerir prioridades. Para ativar:

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4.1-mini"

uvicorn app.main:app --reload
```

Sem a chave, usa heurística local:
- Termos como "urgente", "crítico", "bloqueio" → **urgent**
- Termos como "cliente", "produção", "prazo" → **high**
- Padrão → **medium**

## Códigos HTTP Esperados

| Operação | Status | Descrição |
|----------|--------|-----------|
| GET /health | 200 | Serviço está disponível |
| POST /tasks | 201 | Tarefa criada com sucesso |
| GET /tasks | 200 | Lista de tarefas |
| GET /tasks/{id} | 200 | Tarefa encontrada |
| GET /tasks/{id} | 404 | Tarefa não existe |
| PUT /tasks/{id} | 200 | Tarefa atualizada |
| PUT /tasks/{id} | 404 | Tarefa não existe |
| DELETE /tasks/{id} | 204 | Tarefa deletada |
| DELETE /tasks/{id} | 404 | Tarefa não existe |

## Erros Comuns

### 422 - Validação falhou
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "title"],
      "msg": "title must not be empty"
    }
  ]
}
```

**Causas:**
- `title` vazio ou < 3 caracteres
- `due_date` no passado
- `status` ou `priority` inválido

### 404 - Recurso não encontrado
```json
{
  "detail": "Task not found"
}
```

**Causas:**
- ID não existe
- Tarefa foi deletada

## Próximos Passos

1. **Explorar a documentação interativa:** http://localhost:8000/docs
2. **Rodar os testes:** `pytest -q`
3. **Verificar a implementação:** veja `app/` para entender a arquitetura
4. **Integrar com seu sistema:** use `examples.py` como ponto de partida

## Arquivos de Exemplos

| Arquivo | Descrição | Como usar |
|---------|-----------|-----------|
| `examples.py` | Script Python completo | `python examples.py` |
| `examples.http` | Requisições REST Client/VS Code | Abrir em VS Code com extensão |
| `examples.sh` | Script Bash com curl | `bash examples.sh` |
| `EXEMPLOS.md` | Este arquivo | Referência |

## Suporte

- **API não responde:** Verifique se está rodando: `uvicorn app.main:app --reload`
- **Erro de importação:** Ative o ambiente virtual: `source .venv/bin/activate`
- **Quer testar em outro PC:** Mude `localhost` para o IP do servidor na variável `BASE_URL`

---

**Versão da API:** 0.1.0
**Data:** 3 de maio de 2026
