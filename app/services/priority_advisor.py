import json
import os
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from app.models.task import TaskCreate, TaskPriority, TaskUpdate


class PriorityAdvisor:
    """Suggests task priority with safe fallback."""

    _api_url = "https://api.openai.com/v1/responses"
    _default_model = "gpt-4.1-mini"
    _timeout_seconds = 5

    _urgent_terms = {"urgente", "critico", "crítico", "bloqueio", "incidente"}
    _high_terms = {"importante", "prazo", "cliente", "producao", "produção"}
    _valid_priorities = {priority.value for priority in TaskPriority}

    def suggest(self, payload: TaskCreate | TaskUpdate) -> TaskPriority:
        fallback_priority = self._suggest_locally(payload)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return fallback_priority

        return self._suggest_with_llm(payload, api_key) or fallback_priority

    def _suggest_locally(self, payload: TaskCreate | TaskUpdate) -> TaskPriority:
        content = self._task_content(payload)

        if any(term in content for term in self._urgent_terms):
            return TaskPriority.urgent

        if any(term in content for term in self._high_terms):
            return TaskPriority.high

        return TaskPriority.medium

    def _suggest_with_llm(
        self,
        payload: TaskCreate | TaskUpdate,
        api_key: str,
    ) -> TaskPriority | None:
        request = Request(
            self._api_url,
            data=json.dumps(self._llm_payload(payload)).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except (TimeoutError, URLError, OSError, json.JSONDecodeError):
            return None

        return self._parse_priority(response_data)

    def _llm_payload(self, payload: TaskCreate | TaskUpdate) -> dict[str, Any]:
        model = os.getenv("OPENAI_MODEL", self._default_model)

        return {
            "model": model,
            "input": [
                {
                    "role": "developer",
                    "content": (
                        "Classifique a prioridade da tarefa interna. "
                        "Responda apenas com uma destas palavras: "
                        "low, medium, high, urgent."
                    ),
                },
                {
                    "role": "user",
                    "content": self._task_content(payload),
                },
            ],
            "max_output_tokens": 8,
        }

    def _parse_priority(self, response_data: dict[str, Any]) -> TaskPriority | None:
        text = self._extract_response_text(response_data).strip().lower()
        priority = text.split()[0] if text else ""

        if priority not in self._valid_priorities:
            return None

        return TaskPriority(priority)

    def _extract_response_text(self, response_data: dict[str, Any]) -> str:
        output_text = response_data.get("output_text")
        if isinstance(output_text, str):
            return output_text

        output = response_data.get("output")
        if not isinstance(output, list):
            return ""

        text_parts: list[str] = []
        for item in output:
            if not isinstance(item, dict):
                continue

            content = item.get("content")
            if not isinstance(content, list):
                continue

            for content_item in content:
                if not isinstance(content_item, dict):
                    continue

                text = content_item.get("text")
                if isinstance(text, str):
                    text_parts.append(text)

        return " ".join(text_parts)

    def _task_content(self, payload: TaskCreate | TaskUpdate) -> str:
        return " ".join(
            value
            for value in (payload.title, payload.description)
            if isinstance(value, str)
        ).lower()
