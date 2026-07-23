"""
Edge ↔ Cloud bridge for Silent Sentinel.

Posts pipeline results to a World Monitor instance
(POST /api/silent-sentinel/events).

Configure via config/settings.yaml:

  bridge:
    enabled: true
    url: "http://localhost:3000"          # World Monitor origin
    path: "/api/silent-sentinel/events"
    key: ""                              # optional X-Silent-Sentinel-Key
    timeout_seconds: 10
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


def post_to_worldmonitor(
    results: Dict[str, Any],
    config: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Send a full pipeline result dict to World Monitor.

    Returns the JSON response body on success, or None on failure / when disabled.
    Never raises — bridge failures must not break the edge pipeline.
    """
    bridge_cfg = (config or {}).get("bridge") or {}
    if not bridge_cfg.get("enabled", False):
        return None

    base = str(bridge_cfg.get("url") or "http://localhost:3000").rstrip("/")
    path = str(bridge_cfg.get("path") or "/api/silent-sentinel/events")
    if not path.startswith("/"):
        path = "/" + path
    url = base + path
    key = bridge_cfg.get("key") or ""
    timeout = float(bridge_cfg.get("timeout_seconds") or 10)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "SilentSentinelEdge/0.1",
    }
    if key:
        headers["X-Silent-Sentinel-Key"] = str(key)

    body = json.dumps(results, default=str).encode("utf-8")
    req = Request(url, data=body, headers=headers, method="POST")

    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = {"raw": raw}
            logger.info("Bridge POST ok → %s (status %s)", url, getattr(resp, "status", "?"))
            return parsed if isinstance(parsed, dict) else {"ok": True}
    except HTTPError as e:
        logger.warning("Bridge HTTP error %s: %s", e.code, e.reason)
        return None
    except URLError as e:
        logger.warning("Bridge unreachable (%s): %s", url, e.reason)
        return None
    except Exception as e:  # noqa: BLE001 – never break the pipeline
        logger.warning("Bridge unexpected error: %s", e)
        return None
