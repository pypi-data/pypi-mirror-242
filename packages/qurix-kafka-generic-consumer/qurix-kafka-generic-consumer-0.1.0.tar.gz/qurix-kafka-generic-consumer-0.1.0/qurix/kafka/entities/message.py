from dataclasses import dataclass
from datetime import datetime

from qurix.kafka.entities.base import BaseEntity


@dataclass(frozen=True)
class Message(BaseEntity):
    partition: int
    offset: int
    timestamp: datetime
    length: int
    key: str
    header: bytes
    value: bytes
