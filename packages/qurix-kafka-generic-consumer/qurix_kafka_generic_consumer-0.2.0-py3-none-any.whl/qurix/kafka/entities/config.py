from dataclasses import asdict, dataclass
from enum import Enum
from typing import Callable


class KafkaSecurityProtocol(str, Enum):
    SASL_SL = "SASL_SSL"


class KafkaSaslMechanism(str, Enum):
    PLAIN = "PLAIN"


class Offset(str, Enum):
    EARLIEST = "earliest"
    LATEST = "latest"
    LAST = "last"
    EXPLICIT = "explicit"
    TIMESTAMP = "timestamp"


class BaseConfig:
    def to_dict(self, remove_none_values: bool = True):
        dot_keys_dict = {
            old_key.replace("_", "."): value for old_key, value in asdict(self).items()
        }
        if remove_none_values:
            dot_keys_dict = {k: v for k,
                             v in dot_keys_dict.items() if v is not None}

        return dot_keys_dict


@dataclass
class KafkaBaseConfig(BaseConfig):
    bootstrap_servers: str
    security_protocol: KafkaSecurityProtocol | None = None
    sasl_mechanisms: KafkaSaslMechanism | None = None
    sasl_username: str | None = None
    sasl_password: str | None = None


@dataclass
class ConsumerConfig(KafkaBaseConfig):
    """Properties with default values are not needed in a local environment"""
    group_id: str | None = None
    auto_offset_reset: Offset = Offset.EARLIEST.value
    enable_auto_commit: bool = False
    error_callback: Callable | None = None


@dataclass
class AdminConfig(KafkaBaseConfig):
    pass
