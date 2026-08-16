"""
Exemplos práticos de uso da Task Priority API.

Execute este script com:
    python examples.py

A API deve estar rodando em http://localhost:8000
"""

import httpx
from datetime import datetime, timedelta, UTC

BASE_URL = "http://localhost:8000"


def print_section(title: str) -> None:
    """Print a formatted section title."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def health_check() -> None:
    """Test health endpoint."""
    print_section("1. Health Check")

    response = httpx.get(f"{BASE_URL}/health")
    print(f"GET /health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def create_tasks() -> list[dict]:
    """Create sample tasks and return their data."""
    print_section("2. Criar Tarefas")

    tasks = [
        {
            "title": "Resolver incidente crítico",
            "description": "Falha bloqueando o serviço de produção",
            "status": "pending",
            "priority": "urgent",
            "due_date": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
        },
        {
            "title": "Revisar código da sprint",
            "description": "Validar pull requests do time",
            "status": "pending",
            "priority": "high",
            "due_date": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        },
        {
            "title": "Organizar reunião de planejamento",
            "description": "Agendar e preparar pauta para próxima sprint",
            "status": "pending",
            "priority": "medium",
            "due_date": (datetime.now(UTC) + timedelta(days=3)).isoformat(),
        },
        {
            "title": "Atualizar documentação",
            "description": "Adicionar novos endpoints ao README",
            "status": "pending",
            "priority": "low",
            "due_date": (datetime.now(UTC) + timedelta(days=7)).isoformat(),
        },
    ]

    created_tasks = []
    for task in tasks:
        response = httpx.post(f"{BASE_URL}/tasks", json=task)
        print(f"POST /tasks")
        print(f"Title: {task['title']}")
        print(f"Status: {response.status_code}")
        created_task = response.json()
        print(f"ID: {created_task['id']}")
        print(f"Priority (sugerida): {created_task['priority']}\n")
        created_tasks.append(created_task)

    return created_tasks


def list_all_tasks() -> None:
    """List all tasks without filters."""
    print_section("3. Listar Todas as Tarefas")

    response = httpx.get(f"{BASE_URL}/tasks")
    print(f"GET /tasks")
    print(f"Status: {response.status_code}")
    tasks = response.json()
    print(f"Total de tarefas: {len(tasks)}\n")

    for task in tasks:
        print(f"  • [{task['priority'].upper()}] {task['title']}")
        print(f"    Status: {task['status']}")
        print(f"    ID: {task['id']}\n")


def filter_by_status() -> None:
    """Filter tasks by status."""
    print_section("4. Filtrar Tarefas por Status")

    # Create a task and update it to in_progress
    task_payload = {
        "title": "Implementar novo endpoint",
        "description": "Adicionar rota POST /tasks/suggest",
        "status": "pending",
    }
    response = httpx.post(f"{BASE_URL}/tasks", json=task_payload)
    task = response.json()
    task_id = task["id"]

    # Update status to in_progress
    httpx.put(f"{BASE_URL}/tasks/{task_id}", json={"status": "in_progress"})

    response = httpx.get(f"{BASE_URL}/tasks", params={"status": "in_progress"})
    print(f"GET /tasks?status=in_progress")
    print(f"Status: {response.status_code}")
    tasks = response.json()
    print(f"Tarefas em andamento: {len(tasks)}\n")

    for task in tasks:
        print(f"  • {task['title']} (ID: {task['id']})\n")


def filter_by_priority() -> None:
    """Filter tasks by priority."""
    print_section("5. Filtrar Tarefas por Prioridade")

    for priority in ["urgent", "high", "medium", "low"]:
        response = httpx.get(f"{BASE_URL}/tasks", params={"priority": priority})
        tasks = response.json()

        print(f"GET /tasks?priority={priority}")
        print(f"Total: {len(tasks)}")

        if tasks:
            for task in tasks:
                print(f"  • {task['title']}")
        print()


def get_task_by_id(task_id: str) -> None:
    """Get a specific task by ID."""
    print_section("6. Consultar Tarefa por ID")

    response = httpx.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"GET /tasks/{task_id}")
    print(f"Status: {response.status_code}")
    task = response.json()
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Status: {task['status']}")
    print(f"Priority: {task['priority']}")
    print(f"Created: {task['created_at']}")
    print(f"Updated: {task['updated_at']}\n")


def update_task(task_id: str) -> None:
    """Update a task."""
    print_section("7. Atualizar Tarefa")

    update_payload = {
        "title": "Resolver incidente crítico (ATUALIZADO)",
        "status": "done",
        "priority": "urgent",
    }

    response = httpx.put(f"{BASE_URL}/tasks/{task_id}", json=update_payload)
    print(f"PUT /tasks/{task_id}")
    print(f"Status: {response.status_code}")
    task = response.json()
    print(f"Título atualizado: {task['title']}")
    print(f"Status: {task['status']}")
    print(f"Updated: {task['updated_at']}\n")


def delete_task(task_id: str) -> None:
    """Delete a task."""
    print_section("8. Deletar Tarefa")

    response = httpx.delete(f"{BASE_URL}/tasks/{task_id}")
    print(f"DELETE /tasks/{task_id}")
    print(f"Status: {response.status_code}")
    print(f"Response body: {repr(response.content)}\n")

    # Try to get the deleted task
    response = httpx.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"GET /tasks/{task_id} (após deletion)")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def error_handling() -> None:
    """Demonstrate error handling."""
    print_section("9. Tratamento de Erros")

    # Invalid UUID
    response = httpx.get(f"{BASE_URL}/tasks/invalid-id")
    print(f"GET /tasks/invalid-id (UUID inválido)")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

    # Non-existent task
    response = httpx.get(f"{BASE_URL}/tasks/00000000-0000-0000-0000-000000000000")
    print(f"GET /tasks/00000000-0000-0000-0000-000000000000 (não existe)")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

    # Invalid status
    response = httpx.post(
        f"{BASE_URL}/tasks",
        json={
            "title": "Test task",
            "status": "invalid_status",
        },
    )
    print(f"POST /tasks com status inválido")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def swagger_docs() -> None:
    """Print Swagger/OpenAPI info."""
    print_section("10. Documentação Interativa (Swagger)")

    print("A documentação interativa está disponível em:")
    print("  http://localhost:8000/docs\n")
    print("Redoc (documentação alternativa):")
    print("  http://localhost:8000/redoc\n")


def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 60)
    print("  Task Priority API - Exemplos Práticos de Uso")
    print("=" * 60)
    print("\nCertifique-se que a API está rodando em http://localhost:8000\n")

    try:
        # Basic operations
        health_check()
        created_tasks = create_tasks()
        list_all_tasks()

        # Filtering
        filter_by_status()
        filter_by_priority()

        # Get first task for detailed examples
        if created_tasks:
            first_task_id = created_tasks[0]["id"]
            get_task_by_id(str(first_task_id))
            update_task(str(first_task_id))
            delete_task(str(first_task_id))

        # Error handling
        error_handling()

        # Documentation
        swagger_docs()

        print_section("Resumo")
        print("✓ Todos os exemplos foram executados com sucesso!")
        print("\nTips:")
        print("  • Visualize a API em tempo real: http://localhost:8000/docs")
        print("  • O projeto suporta variável OPENAI_API_KEY para priorização com IA")
        print("  • Em caso de erro na IA, usa heurística local como fallback")
        print()

    except httpx.ConnectError:
        print("\n❌ Erro: Não foi possível conectar à API em http://localhost:8000")
        print("Certifique-se que a API está rodando com:")
        print("  uvicorn app.main:app --reload\n")
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")


if __name__ == "__main__":
    main()
