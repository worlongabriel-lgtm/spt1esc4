# Backlog Minimo

## Release 1 - Core

- [ ] **RF01 - Health check da API**
  - Disponibilizar endpoint `GET /health`.
  - Retornar status da aplicacao e timestamp da requisicao.
  - **Criterios de aceite:**
    - [ ] A rota `/health` responde com HTTP `200`.
    - [ ] A resposta contem `status` com valor `ok`.
    - [ ] A resposta contem `timestamp` em formato ISO 8601.

- [ ] **RF02 - Criar tarefa**
  - Permitir cadastro de uma nova tarefa.
  - Campos minimos: `title`, `description`, `status`, `priority`, `due_date`.
  - **Criterios de aceite:**
    - [ ] A API cria uma tarefa valida.
    - [ ] A tarefa criada recebe identificador unico.
    - [ ] Campos obrigatorios ausentes retornam erro HTTP `422`.

- [ ] **RF03 - Listar tarefas**
  - Permitir consulta das tarefas cadastradas.
  - **Criterios de aceite:**
    - [ ] A API retorna uma lista de tarefas.
    - [ ] Quando nao houver tarefas, retorna lista vazia.
    - [ ] Cada item retorna os campos principais da tarefa.

- [ ] **RF04 - Consultar tarefa por ID**
  - Permitir busca de uma tarefa por identificador.
  - **Criterios de aceite:**
    - [ ] A API retorna a tarefa quando o ID existe.
    - [ ] A API retorna HTTP `404` quando o ID nao existe.

- [ ] **RF05 - Atualizar tarefa**
  - Permitir alteracao dos dados principais de uma tarefa.
  - **Criterios de aceite:**
    - [ ] A API atualiza uma tarefa existente.
    - [ ] A API preserva o identificador original.
    - [ ] A API atualiza o campo `updated_at`.
    - [ ] A API retorna HTTP `404` quando o ID nao existe.

- [ ] **RF06 - Remover tarefa**
  - Permitir remocao de uma tarefa por identificador.
  - **Criterios de aceite:**
    - [ ] A API remove uma tarefa existente.
    - [ ] Consultar a tarefa removida retorna HTTP `404`.
    - [ ] Remover ID inexistente retorna HTTP `404`.

- [ ] **RT01 - Estrutura base do projeto**
  - Organizar o projeto com separacao minima entre aplicacao, modelos e testes.
  - **Criterios de aceite:**
    - [ ] O projeto executa com `uvicorn app.main:app --reload`.
    - [ ] O projeto possui `requirements.txt`.
    - [ ] O projeto possui README com instrucoes de execucao.

## Release 2 - Qualidade

- [ ] **RF07 - Validacao de dados**
  - Garantir validacoes de entrada para os campos de tarefa.
  - **Criterios de aceite:**
    - [ ] `title` nao aceita valor vazio.
    - [ ] `status` aceita apenas valores previstos.
    - [ ] `priority` aceita apenas valores previstos.
    - [ ] Datas invalidas retornam erro HTTP `422`.

- [ ] **RF08 - Filtros de listagem**
  - Permitir filtros basicos na listagem de tarefas.
  - Filtros previstos: `status`, `priority`, `due_date`.
  - **Criterios de aceite:**
    - [ ] A API filtra tarefas por status.
    - [ ] A API filtra tarefas por prioridade.
    - [ ] A API filtra tarefas por prazo.
    - [ ] Filtros invalidos retornam erro consistente.

- [ ] **RT02 - Testes automatizados**
  - Cobrir endpoints principais com testes.
  - **Criterios de aceite:**
    - [ ] Existem testes para `/health`.
    - [ ] Existem testes para CRUD de tarefas.
    - [ ] A suite roda com `pytest`.
    - [ ] Testes falham quando contrato esperado e quebrado.

- [ ] **RT03 - Tratamento padronizado de erros**
  - Padronizar respostas de erro da API.
  - **Criterios de aceite:**
    - [ ] Erros de validacao retornam HTTP `422`.
    - [ ] Recursos inexistentes retornam HTTP `404`.
    - [ ] Erros possuem mensagem objetiva para o consumidor.

- [ ] **RT04 - Configuracao por ambiente**
  - Carregar configuracoes por variaveis de ambiente.
  - **Criterios de aceite:**
    - [ ] O projeto suporta arquivo `.env` local.
    - [ ] Segredos nao sao versionados.
    - [ ] Variaveis esperadas sao documentadas.

## Release 3 - Entrega Final

- [ ] **RF09 - Priorizacao assistida por IA**
  - Disponibilizar recurso para sugerir prioridade de uma tarefa.
  - **Criterios de aceite:**
    - [ ] A API recebe dados da tarefa e contexto adicional.
    - [ ] A API retorna prioridade sugerida.
    - [ ] A resposta inclui justificativa curta da sugestao.
    - [ ] Falha na IA retorna erro tratado.

- [ ] **RF10 - Documentacao dos endpoints**
  - Garantir documentacao clara via OpenAPI/Swagger.
  - **Criterios de aceite:**
    - [ ] Todos os endpoints possuem schema de entrada e saida.
    - [ ] Os principais codigos HTTP estao representados.
    - [ ] A documentacao pode ser acessada em `/docs`.

- [ ] **RT05 - Logs basicos**
  - Registrar eventos relevantes da aplicacao.
  - **Criterios de aceite:**
    - [ ] Inicializacao da API gera log.
    - [ ] Erros de aplicacao geram log.
    - [ ] Logs nao expõem segredos.

- [ ] **RT06 - Preparacao para deploy**
  - Preparar configuracoes minimas para entrega controlada.
  - **Criterios de aceite:**
    - [ ] Dependencias estao declaradas no `requirements.txt`.
    - [ ] Comando de start da aplicacao esta documentado.
    - [ ] Variaveis obrigatorias estao documentadas.
    - [ ] O projeto inicia sem depender de arquivos locais sensiveis.

- [ ] **RT07 - Revisao final de qualidade**
  - Validar consistencia da entrega antes da release final.
  - **Criterios de aceite:**
    - [ ] Testes automatizados executam com sucesso.
    - [ ] README esta atualizado.
    - [ ] Escopo do MVP esta atualizado.
    - [ ] Backlog reflete o estado esperado das releases.
