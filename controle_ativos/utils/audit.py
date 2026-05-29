import logging
from collections import deque
from datetime import datetime
from typing import Any, Dict, Optional
import json

LOGGER_NAME = "controle_ativos.audit"
logger = logging.getLogger(LOGGER_NAME)
RECENT_EVENTS = deque(maxlen=50)


def _scrub_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove keys that may contain sensitive values."""
    if not d:
        return d
    scrubbed = {}
    sensitive_keys = {"senha", "password", "resposta", "csrf_token", "token", "secret", "secret_key", "pepper"}
    for k, v in d.items():
        if any(sk in k.lower() for sk in sensitive_keys):
            scrubbed[k] = "[REDACTED]"
        else:
            scrubbed[k] = v
    return scrubbed


def audit_event(
    event: str,
    result: str,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
    ip: Optional[str] = None,
    route: Optional[str] = None,
    method: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
):
    """Emit a structured audit event to the audit logger.

    The function avoids emitting sensitive values and keeps payloads
    JSON-serializable.
    """
    payload: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event,
        "result": result,
    }

    if user_id is not None:
        payload["user_id"] = int(user_id)
    if email is not None:
        payload["email"] = (email or "").strip().lower()
    if ip is not None:
        payload["ip"] = ip
    if route is not None:
        payload["route"] = route
    if method is not None:
        payload["method"] = method

    if extra:
        payload["extra"] = _scrub_dict(extra)

    logger.info(json.dumps(payload, ensure_ascii=False, default=str))

    RECENT_EVENTS.appendleft(payload)


def get_recent_events(limit: int = 20) -> list[Dict[str, Any]]:
    """Retorna uma janela recente dos eventos de auditoria disponíveis."""
    limit = max(0, min(int(limit), len(RECENT_EVENTS)))
    return list(RECENT_EVENTS)[:limit]
