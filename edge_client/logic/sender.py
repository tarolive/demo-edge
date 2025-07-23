import logging, requests
from typing import Dict, Any
from src import config

log = logging.getLogger("edge_client.sender")
ENDPOINT = f"{config.EDGE_SERVER.rstrip('/')}/inference"


def post_detection(payload: Dict[str, Any]) -> None:
    """
    Fire-and-forget POST; raises for non-2xx HTTP codes.
    """
    resp = requests.post(ENDPOINT, json=payload, timeout=5)
    resp.raise_for_status()
    log.debug("Posted detection (%s) → %s", payload.get("labels"), ENDPOINT)
