import time
from typing import Any, Optional

class Cache:
    def __init__(self):
        self.data: dict[str, tuple[Any, float]] = {}
        self.ttl = 86400  # 24 hours

    def get(self, key: str) -> Optional[Any]:
        if key not in self.data:
            return None
        value, timestamp = self.data[key]
        if time.time() - timestamp > self.ttl:
            del self.data[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self.data[key] = (value, time.time())

    def clear(self) -> None:
        self.data.clear()

cache = Cache()
