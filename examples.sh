#!/bin/bash

# Task Priority API - Exemplos com curl
#
# Certifique-se que a API está rodando em http://localhost:8000
# Execute este script com: bash examples.sh

BASE_URL="http://localhost:8000"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir seções
print_section() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================${NC}\n"
}

# Função para imprimir comandos
print_command() {
    echo -e "${YELLOW}$ $1${NC}"
}

# Função para formatar JSON output
format_json() {
    if command -v jq &> /dev/null; then
        jq '.'
    else
        cat
    fi
}

# 1. Health Check
print_section "1. Health Check"
print_command "curl -s -X GET $BASE_URL/health | jq"
curl -s -X GET "$BASE_URL/health" | format_json

# 2. Criar primeira tarefa (urgente)
print_section "2. Criar tarefa urgente"
TASK1_JSON=$(cat <<EOF
{
  "title": "Resolver incidente crítico",
  "description": "Falha bloqueando serviço de produção",
  "status": "pending"
}
EOF
)
print_command "curl -s -X POST $BASE_URL/tasks -H \"Content-Type: application/json\" -d '$TASK1_JSON' | jq"
TASK1=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d "$TASK1_JSON" | format_json)
echo "$TASK1"

# Extrair ID da primeira tarefa (usando jq se disponível)
if command -v jq &> /dev/null; then
    TASK1_ID=$(echo "$TASK1" | jq -r '.id')
else
    TASK1_ID=$(echo "$TASK1" | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
fi

# 3. Criar segunda tarefa (alta prioridade)
print_section "3. Criar tarefa com prazo"
TASK2_JSON=$(cat <<EOF
{
  "title": "Revisar código da sprint",
  "description": "Validar pull requests",
  "due_date": "2026-05-04T18:00:00Z"
}
EOF
)
print_command "curl -s -X POST $BASE_URL/tasks -H \"Content-Type: application/json\" -d '$TASK2_JSON' | jq"
curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d "$TASK2_JSON" | format_json

# 4. Criar terceira tarefa
print_section "4. Criar tarefa simples"
TASK3_JSON=$(cat <<EOF
{
  "title": "Organizar reunião de planejamento",
  "description": "Agendar pauta para sprint"
}
EOF
)
print_command "curl -s -X POST $BASE_URL/tasks -H \"Content-Type: application/json\" -d '$TASK3_JSON' | jq"
curl -s -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d "$TASK3_JSON" | format_json

# 5. Listar todas as tarefas
print_section "5. Listar todas as tarefas"
print_command "curl -s -X GET $BASE_URL/tasks | jq '.[] | {id: .id, title: .title, priority: .priority, status: .status}'"
curl -s -X GET "$BASE_URL/tasks" | \
  (if command -v jq &> /dev/null; then jq '.[] | {id: .id, title: .title, priority: .priority, status: .status}'; else cat; fi)

# 6. Filtrar por prioridade urgente
print_section "6. Filtrar tarefas por prioridade=urgent"
print_command "curl -s -X GET \"$BASE_URL/tasks?priority=urgent\" | jq '.[] | {title, priority}'"
curl -s -X GET "$BASE_URL/tasks?priority=urgent" | \
  (if command -v jq &> /dev/null; then jq '.[] | {title: .title, priority: .priority}'; else cat; fi)

# 7. Filtrar por status pending
print_section "7. Filtrar tarefas por status=pending"
print_command "curl -s -X GET \"$BASE_URL/tasks?status=pending\" | jq '.[] | {title, status}'"
curl -s -X GET "$BASE_URL/tasks?status=pending" | \
  (if command -v jq &> /dev/null; then jq '.[] | {title: .title, status: .status}'; else cat; fi)

# 8. Consultar tarefa específica por ID
if [ ! -z "$TASK1_ID" ]; then
    print_section "8. Consultar tarefa por ID"
    print_command "curl -s -X GET $BASE_URL/tasks/$TASK1_ID | jq"
    curl -s -X GET "$BASE_URL/tasks/$TASK1_ID" | format_json

    # 9. Atualizar tarefa
    print_section "9. Atualizar tarefa"
    UPDATE_JSON=$(cat <<EOF
{
  "title": "Resolver incidente crítico (RESOLVIDO)",
  "status": "done",
  "priority": "urgent"
}
EOF
)
    print_command "curl -s -X PUT $BASE_URL/tasks/$TASK1_ID -H \"Content-Type: application/json\" -d '$UPDATE_JSON' | jq"
    curl -s -X PUT "$BASE_URL/tasks/$TASK1_ID" \
      -H "Content-Type: application/json" \
      -d "$UPDATE_JSON" | format_json

    # 10. Deletar tarefa
    print_section "10. Deletar tarefa"
    print_command "curl -s -i -X DELETE $BASE_URL/tasks/$TASK1_ID"
    curl -s -i -X DELETE "$BASE_URL/tasks/$TASK1_ID"

    # 11. Tentar consultar tarefa deletada (deve retornar 404)
    print_section "11. Consultar tarefa deletada (deve retornar 404)"
    print_command "curl -s -w \"\\nStatus: %{http_code}\\n\" -X GET $BASE_URL/tasks/$TASK1_ID | jq"
    curl -s -w "\nStatus: %{http_code}\n" -X GET "$BASE_URL/tasks/$TASK1_ID" | format_json
else
    echo -e "${RED}Erro: Não foi possível extrair o ID da tarefa${NC}"
fi

# 12. Testes de erro - UUID inválido
print_section "12. Teste de erro: UUID inválido (deve retornar 422)"
print_command "curl -s -w \"\\nStatus: %{http_code}\\n\" -X GET $BASE_URL/tasks/invalid-uuid | jq"
curl -s -w "\nStatus: %{http_code}\n" -X GET "$BASE_URL/tasks/invalid-uuid" | format_json

# 13. Testes de erro - Tarefa não existente
print_section "13. Teste de erro: Tarefa não existente (deve retornar 404)"
print_command "curl -s -w \"\\nStatus: %{http_code}\\n\" -X GET $BASE_URL/tasks/00000000-0000-0000-0000-000000000000 | jq"
curl -s -w "\nStatus: %{http_code}\n" -X GET "$BASE_URL/tasks/00000000-0000-0000-0000-000000000000" | format_json

# 14. Testes de erro - Status inválido
print_section "14. Teste de erro: Status inválido (deve retornar 422)"
INVALID_JSON=$(cat <<EOF
{
  "title": "Teste",
  "status": "invalid_status"
}
EOF
)
print_command "curl -s -w \"\\nStatus: %{http_code}\\n\" -X POST $BASE_URL/tasks -H \"Content-Type: application/json\" -d '$INVALID_JSON' | jq"
curl -s -w "\nStatus: %{http_code}\n" -X POST "$BASE_URL/tasks" \
  -H "Content-Type: application/json" \
  -d "$INVALID_JSON" | format_json

# Summary
print_section "Resumo"
echo -e "${GREEN}✓ Exemplos executados com sucesso!${NC}"
echo ""
echo "Tips:"
echo "  • Documentação interativa: $BASE_URL/docs"
echo "  • ReDoc: $BASE_URL/redoc"
echo "  • Para melhor formatação, instale 'jq': sudo apt install jq"
echo ""
