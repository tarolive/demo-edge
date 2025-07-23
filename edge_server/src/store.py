from collections import defaultdict, deque
from typing import Dict, Deque
from asyncio import Lock
from src.config import MAX_HISTORY

_store: Dict[str, Deque[dict]] = defaultdict(lambda: deque(maxlen=MAX_HISTORY))
_lock = Lock()        # async Lock because FastAPI handlers are async


async def add(edge_id: str, payload: dict) -> None:
    """Append a detection to the store (keeps last MAX_HISTORY per edge)."""
    async with _lock:
        _store[edge_id].appendleft(payload)


async def snapshot() -> dict:
    """Return *copy* of current state (for Streamlit)."""
    async with _lock:
        # shallow copies are fine because UI is read-only
        return {k: list(v) for k, v in _store.items()}
