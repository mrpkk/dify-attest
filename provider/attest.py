from __future__ import annotations

from typing import Any

import requests

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

DEFAULT_BASE = "https://attest.rta.lat"


class AttestProvider(ToolProvider):
    """Провайдер attest. Проверка креденшелов не тратит платные вызовы.

    Валидируем только /health: GET бесплатен и не расходует ни бесплатный
    лимит проверок, ни x402. Валидация через сам /verify стоила бы вызова
    (а на исчерпанном лимите — вообще 402), и установка плагина падала бы
    у честного пользователя с непонятной ошибкой.
    """

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        base = (credentials.get("api_base") or DEFAULT_BASE).rstrip("/")
        if not base.startswith(("http://", "https://")):
            raise ToolProviderCredentialValidationError(
                "api_base must be an absolute http(s) URL")
        try:
            response = requests.get(f"{base}/health", timeout=10,
                                    headers={"User-Agent": "dify-attest-plugin/0.0.1"})
            response.raise_for_status()
        except Exception as exc:  # noqa: BLE001 — наружу отдаём причину строкой
            raise ToolProviderCredentialValidationError(
                f"attest is not reachable at {base}: {exc}") from exc
