1. Inicialização e Gitignore
Contexto: Estou iniciando uma API Python com FastAPI em um repositório de produto.
Objetivo: Criar o arquivo .gitignore contemplando arquivos do Python, ambiente virtual, cache de testes e configurações locais do editor.
Estilo: Organizado por seções e com comentários explicativos.
Resposta: Forneça apenas o código com o conteúdo do arquivo .gitignore.

2. Versionamento
Contexto: A estrutura inicial do projeto e o .gitignore estão prontos.
Objetivo: Iniciar o versionamento do projeto com Git.
Estilo: Comandos de terminal diretos e concisos.
Resposta: Execute os comandos Bash para inicializar o repositório (git init) e preparar a base do projeto.

3. Readme Inicial
Contexto: Repositório recém-criado para uma API de tarefas em FastAPI.
Objetivo: Criar um arquivo README.md base com o título do projeto, uma breve descrição e instruções iniciais.
Estilo: Markdown simples e direto.
Resposta: Forneça o conteúdo do arquivo README.md.

4. Setup do FastAPI
Contexto: O projeto base está criado.
Objetivo: Criar o arquivo app/main.py com uma instância do FastAPI e um endpoint GET /health que retorne o status "ok" e o timestamp atual.
Estilo: Código limpo, utilizando tipagem estática.
Resposta: Forneça o código completo para o arquivo app/main.py.

5. Dependências
Contexto: A API usa FastAPI, Uvicorn, Pydantic e lida com variáveis de ambiente.
Objetivo: Criar o arquivo requirements.txt com as dependências necessárias para rodar o projeto.
Estilo: Lista limpa e direta com as bibliotecas essenciais e suas versões (opcional).
Resposta: Forneça o conteúdo do arquivo requirements.txt.

6. Commit de Base
Contexto: Adicionei a estrutura inicial, README.md, .gitignore, requirements.txt e o endpoint /health. (Veja também qualquer outra alteração não listada).
Objetivo: Gerar uma mensagem de commit seguindo o padrão Conventional Commits para registrar essas adições.
Estilo: Padrão Conventional Commits (ex: feat:, chore:, docs:).
Resposta: Forneça apenas uma linha com a mensagem de commit e realize o commit no sistema com esta mensagem.

7. Documentação do Escopo
Contexto: Estamos construindo o MVP de uma micro-API de tarefas para uso de uma equipe interna.
Objetivo: Gerar um documento de escopo definindo o objetivo do projeto, requisitos funcionais, requisitos não funcionais e o que está fora do escopo.
Estilo: Linguagem técnica, direta e estruturada em Markdown.
Resposta: Forneça o conteúdo completo para o arquivo docs/escopo-mvp.md.

8. Backlog e Releases
Contexto: O produto será entregue em 3 releases: Core, Qualidade e Entrega Final.
Objetivo: Criar um backlog mínimo estruturado pelas releases, contendo IDs (RF/RT) e critérios de aceite para as tarefas.
Estilo: Formato de checklist em Markdown.
Resposta: Forneça o conteúdo completo para o arquivo docs/backlog.md.

9. Arquitetura em Diagrama
Contexto: A API utiliza FastAPI e possui uma arquitetura dividida em camadas: API (rotas), Service, Repository e um componente externo chamado PriorityAdvisor.
Objetivo: Gerar um diagrama de componentes e fluxo de dados utilizando a sintaxe do Mermaid.
Estilo: Diagrama simples, legível e que mostre claramente a direção dos dados.
Resposta: Forneça o código Mermaid para ser criado no arquivo docs/diagrama-componentes.md.

10. Regra de Commits
Contexto: Desenvolvimento contínuo do projeto.
Objetivo: Definir a regra de que todas as futuras mensagens de commit devem obrigatoriamente seguir o padrão Conventional Commits.
Estilo: Instrução de comportamento.
Resposta: Apenas confirme que a instrução foi compreendida e será aplicada automaticamente nos próximos commits.

11. Modelos (Schemas)
Contexto: API de tarefas em FastAPI para uso interno de equipe.
Objetivo: Criar os modelos TaskCreate, TaskUpdate e TaskOut com tipagem estática e validações de dados.
Estilo: Utilizar Pydantic v2, código limpo e docstrings curtas.
Resposta: Forneça o código completo para criar o arquivo app/models/task.py.

12. Persistência de Dados
Contexto: Preciso de uma persistência de dados inicial e enxuta para viabilizar a primeira release de forma ágil.
Objetivo: Criar a classe TaskRepository persistindo os dados em memória com os métodos: create, list, get_by_id, update e delete.
Estilo: Python tipado, focado e sem dependências de bibliotecas de banco de dados.
Resposta: Forneça o código completo para o arquivo app/repository/task_repository.py.

13. Lógica de Negócio (Service e Advisor Base)
Contexto: A prioridade da tarefa pode ser sugerida automaticamente pelo sistema.
Objetivo: Criar a classe TaskService que utilize o TaskRepository e orquestre as chamadas para um novo módulo PriorityAdvisor.
Estilo: Arquitetura em camadas, isolando estritamente a regra de negócio da camada de API.
Resposta: Forneça os códigos para app/services/task_service.py e a base inicial de app/services/priority_advisor.py.

14. Integração com IA e Resiliência
Contexto: Quero que o sistema rode sem custos de API quando não houver chave configurada.
Objetivo: Implementar no PriorityAdvisor uma heurística de texto local e a capacidade de fazer chamadas à LLM (OpenAI) de forma opcional (apenas se a variável OPENAI_API_KEY existir).
Estilo: Arquitetura com falha segura (fail-safe), implementando timeout para requisições externas e fallback obrigatório para a heurística local.
Resposta: Forneça o código atualizado de app/services/priority_advisor.py.

15. Controladores (Rotas)
Contexto: A estrutura do FastAPI com o TaskService completo já está pronta.
Objetivo: Criar as rotas da API (POST, GET, PUT, DELETE) para gerenciar tarefas, retornando os status HTTP corretos (201, 200, 204) e tratando exceções (como 404).
Estilo: Utilizar APIRouter separado em app/api/task_routes.py.
Resposta: Forneça o arquivo com o código e as instruções de como registrá-lo no app/main.py.

16. Filtros de Listagem
Contexto: A rota GET /tasks lista todas as tarefas e a arquitetura possui camadas.
Objetivo: Adicionar filtros básicos por status e priority na listagem de tarefas (API, Service e Repository).
Estilo: FastAPI query parameters opcionais com tipagem e código limpo.
Resposta: Forneça as alterações para app/api/task_routes.py, app/services/task_service.py e app/repository/task_repository.py.

17. Testes Unificados e Análise (Cobertura Total)
Contexto: A API possui rotas, um serviço (TaskService), um repositório em memória e o componente PriorityAdvisor com heurística e fallback seguro. Objetivo:

Gerar os testes unitários (test_task_service.py) cobrindo o CRUD e casos de ID inexistente.
Gerar os testes do Advisor (test_priority_advisor.py) cobrindo os níveis de prioridade e o comportamento do fallback usando monkeypatch.
Gerar os testes de integração (test_task_routes.py) com TestClient para validar os status HTTP, isolando o estado global do repositório.
Analisar o projeto e sugerir quais outros tipos de testes (ex: testes de contrato, carga) fariam sentido futuramente.
Estilo: Nomes de testes descritivos, fixtures simples e código Pytest limpo.
Resposta: Forneça os códigos dos três arquivos de testes e liste as sugestões de novos testes.

18. Automação com Makefile
Contexto: O projeto já possui a API, banco em memória e uma bateria de testes pronta. Para facilitar o dia a dia, precisamos automatizar a execução.
Objetivo: Criar um arquivo Makefile com comandos (targets) para: criar o ambiente virtual e instalar dependências (make install), rodar os testes (make test), iniciar o servidor FastAPI localmente (make run)e limpar arquivos de cache/temporários (make clean).
Estilo: Simples, declarativo e que garanta a detecção correta do ambiente virtual (.venv ou venv).
Resposta: Forneça apenas o código completo para o arquivo Makefile.

19. Verificação de Segurança (Risco de Exposição)
Contexto: O projeto utiliza variáveis de ambiente para chaves de IA (OpenAI) e pode lidar com configurações sensíveis.
Objetivo: Fazer uma varredura profunda no projeto em busca de riscos de exposição de dados sensíveis (ex: chaves hardcoded, tokens em logs ou arquivos .env faltando no .gitignore).
Estilo: Verificação de segurança rigorosa e preventiva.
Resposta: Execute os comandos de busca (ex: grep), relate o status da verificação e, se encontrar vulnerabilidades, corrija-as (como atualizar o .gitignore ou criar um .env.example).

20. Análise Técnica e Checklist
Contexto: O código e os testes atuais formam a base do nosso MVP.
Objetivo: Avaliar o código e gerar um checklist técnico contendo: riscos técnicos restantes na arquitetura atual, gaps na cobertura de testes e as melhorias mais prioritárias para a próxima release.
Estilo: Formato de bullet points curtos e diretos.
Resposta: Forneça o conteúdo e crie o arquivo checklist-proxima-release.txt.

21. Prova de Conceito (Exemplos Práticos)
Contexto: Eu gostaria de ver a API funcionando na prática.
Objetivo: Executar a API em segundo plano e gerar exemplos reais de clientes interagindo com os endpoints de criação, listagem e atualização.
Estilo: Demonstração prática via terminal ou script.
Resposta: Forneça e execute as requisições na própria conversa (usando comandos curl ou um script Python examples.py), mostrando os dados entrando e a resposta real da API.

22. Documentação Final
Contexto: O MVP da micro-API de tarefas com prioridade assistida por IA está pronto e validado.
Objetivo: Gerar o arquivo README.md completo e definitivo contendo: visão geral do sistema, instruções de instalação (incluindo o uso do Makefile), comandos de execução, como rodar testes, explicação técnica da arquitetura, o funcionamento da IA (com fallback opcional), limitações e os próximos passos mapeados.
Estilo: Markdown profissional, objetivo e altamente técnico.
Resposta: Forneça o código completo para substituir o conteúdo do README.md.