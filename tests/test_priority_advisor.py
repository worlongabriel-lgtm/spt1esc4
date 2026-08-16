from urllib.error import URLError

from app.models.task import TaskCreate, TaskPriority
from app.services import priority_advisor
from app.services.priority_advisor import PriorityAdvisor


def test_suggest_returns_urgent_priority_for_urgent_terms(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    advisor = PriorityAdvisor()
    payload = TaskCreate(
        title="Resolver incidente critico",
        description="Servico interno com bloqueio para a equipe",
    )

    priority = advisor.suggest(payload)

    assert priority == TaskPriority.urgent


def test_suggest_returns_high_priority_for_high_impact_terms(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    advisor = PriorityAdvisor()
    payload = TaskCreate(
        title="Revisar prazo do cliente",
        description="Atividade importante para entrega interna",
    )

    priority = advisor.suggest(payload)

    assert priority == TaskPriority.high


def test_suggest_returns_medium_priority_by_default(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    advisor = PriorityAdvisor()
    payload = TaskCreate(
        title="Organizar notas da reuniao",
        description="Consolidar pontos discutidos pelo time",
    )

    priority = advisor.suggest(payload)

    assert priority == TaskPriority.medium


def test_suggest_falls_back_to_local_priority_when_llm_call_fails(monkeypatch) -> None:
    def raise_network_error(*args, **kwargs):
        raise URLError("network unavailable")

    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setattr(priority_advisor, "urlopen", raise_network_error)

    advisor = PriorityAdvisor()
    payload = TaskCreate(
        title="Resolver incidente urgente",
        description="Falha bloqueando rotina interna",
    )

    priority = advisor.suggest(payload)

    assert priority == TaskPriority.urgent
