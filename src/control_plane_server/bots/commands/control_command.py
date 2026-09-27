from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid7

@dataclass(kw_only=True)
class ControlCommand():
    message_id: UUID = field(default_factory=uuid7)
    trace_id: str = field(default_factory=lambda: str(uuid7()))
    timestamp: str = field(
    default_factory=lambda: datetime.now(timezone.utc)
    .isoformat(timespec="milliseconds")
    .replace("+00:00", "Z")
)
