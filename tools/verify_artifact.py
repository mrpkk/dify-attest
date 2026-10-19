from __future__ import annotations

import json
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

DEFAULT_BASE = "https://attest.rta.lat"
USER_AGENT = "dify-attest-plugin/0.0.1"


def _as_json(value: Any, field: str) -> Any:
    """Строка → JSON, если это валидный JSON; иначе исходная строка.

    Артефакт может быть обычной строкой (текст от инструмента) — это
    легальный вход, поэтому ошибку разбора здесь не поднимаем. А вот
    schema — это контракт; если её не разобрать, отправлять мусор нельзя.
    """
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        if field == "schema":
            raise ValueError("schema must be valid JSON (JSON Schema)")
        return value


class VerifyArtifactTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        base = (self.runtime.credentials.get("api_base") or DEFAULT_BASE).rstrip("/")
        payload: dict[str, Any] = {"artifact": _as_json(tool_parameters["artifact"], "artifact")}
        schema_raw = tool_parameters.get("schema")
        if schema_raw:
            payload["schema"] = _as_json(schema_raw, "schema")

        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        entitlement = self.runtime.credentials.get("entitlement")
        if entitlement:
            headers["X-ATTEST-ENTITLEMENT"] = str(entitlement)

        response = requests.post(f"{base}/verify", json=payload, headers=headers, timeout=25)

        # 402 — это честное «лимит кончился», а не поломка: отдаём телу дойти
        # до пользователя с тем же JSON, что прислал сервис.
        try:
            data = response.json()
        except ValueError:
            data = {"status": response.status_code, "body": response.text[:2000]}

        if not response.ok and not isinstance(data, dict):
            data = {"status": response.status_code, "body": str(data)}
        yield self.create_json_message(data)
