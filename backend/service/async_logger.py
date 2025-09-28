import asyncio
from datetime import datetime

class AsyncLogger:
    """
    Uniform async logger for Mailopolis backend.
    Supports log history, async subscribers, and pluggable sinks (e.g., ws, file, stdout).
    """
    def __init__(self, buffer_size=500):
        self._log_history = []
        self._subscribers = []  # List of asyncio.Queue
        self._buffer_size = buffer_size

    def log(self, message: str):
        ts = datetime.utcnow().isoformat()
        full = f"[{ts}] {message}"
        # Store in history
        self._log_history.append(full)
        if len(self._log_history) > self._buffer_size:
            self._log_history.pop(0)
        # Print to stdout
        print(full)
        # Send to subscribers
        for q in list(self._subscribers):
            try:
                q.put_nowait(full)
            except Exception:
                try:
                    asyncio.create_task(q.put(full))
                except Exception:
                    continue

    async def subscribe(self) -> asyncio.Queue:
        q = asyncio.Queue()
        self._subscribers.append(q)
        # Send history
        for item in self._log_history:
            try:
                q.put_nowait(item)
            except Exception:
                await q.put(item)
        return q

    async def unsubscribe(self, q: asyncio.Queue):
        try:
            self._subscribers.remove(q)
        except ValueError:
            pass
