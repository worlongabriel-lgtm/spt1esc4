# Task Priority API

Micro-API para gestao de tarefas com priorizacao assistida por IA.

## Objetivo

Este projeto tem como objetivo entregar um MVP de API para cadastro, consulta e organizacao de tarefas, com suporte a priorizacao assistida por IA.

A proposta e ajudar usuarios ou sistemas consumidores a identificar quais tarefas merecem mais atencao com base em criterios como urgencia, impacto, prazo e contexto informado.

## Stack

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- Ambiente virtual com `venv`

## Funcionalidades previstas no MVP

- Criar tarefas
- Listar tarefas
- Consultar uma tarefa por identificador
- Atualizar status, titulo, descricao e prazo
- Remover tarefas
- Classificar prioridade da tarefa com apoio de IA
- Expor documentacao interativa via Swagger/OpenAPI

## Como rodar localmente

### 1. Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv .venv
```

### 3. Ativar o ambiente virtual

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install fastapi uvicorn pytest
```

Quando o arquivo `requirements.txt` estiver disponivel, use:

```bash
pip install -r requirements.txt
```

### 5. Rodar a API

```bash
uvicorn app.main:app --reload
```

A API ficara disponivel em:

```text
http://localhost:8000
```

Documentacao interativa:

```text
http://localhost:8000/docs
```

## Variaveis de ambiente

Crie um arquivo `.env` na raiz do projeto para configuracoes locais.

Exemplo:

```env
APP_ENV=local
APP_NAME=Task Priority API
AI_PROVIDER=openai
AI_MODEL=<modelo-de-ia>
AI_API_KEY=<sua-chave>
```

O arquivo `.env` nao deve ser versionado. Use `.env.example` para compartilhar variaveis esperadas sem expor segredos.

## Testes

Para executar os testes:

```bash
pytest
```

## Roadmap de release

### v0.1.0 - Base da API

- Estrutura inicial do projeto FastAPI
- Endpoint de health check
- Modelo inicial de tarefa
- Rotas basicas de CRUD em memoria
- README e configuracoes iniciais de desenvolvimento

### v0.2.0 - Persistencia e validacoes

- Persistencia em banco de dados
- Configuracao por variaveis de ambiente
- Validacoes de entrada com Pydantic
- Testes unitarios para regras principais

### v0.3.0 - Priorizacao assistida por IA

- Integracao com provedor de IA
- Endpoint para sugerir prioridade de tarefas
- Criterios de priorizacao configuraveis
- Tratamento de falhas na chamada externa de IA

### v0.4.0 - Pronto para homologacao

- Logs estruturados
- Testes de integracao
- Documentacao dos endpoints
- Ajustes de seguranca e configuracao para deploy

## Status do projeto

Projeto em fase inicial de MVP.
