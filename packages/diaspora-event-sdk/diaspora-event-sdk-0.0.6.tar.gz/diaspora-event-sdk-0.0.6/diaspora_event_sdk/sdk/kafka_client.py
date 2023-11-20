import json
from typing import Dict, Any
import warnings

from ._environments import MSK_SCRAM_ENDPOINT
from .client import Client

# Flag to indicate if kafka-python is available
kafka_available = True
try:
    from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
    from kafka.admin import NewTopic
except ImportError:
    kafka_available = False


def get_diaspora_config(extra_configs: Dict[str, Any] = {}) -> Dict[str, Any]:
    """
    Retrieve default Diaspora event fabric connection configurations for Kafka clients.
    Merges default configurations with custom ones provided.
    """
    try:
        keys = Client().retrieve_key()
    except Exception as e:
        raise RuntimeError("Failed to retrieve Kafka keys") from e

    conf = {
        "bootstrap_servers":  MSK_SCRAM_ENDPOINT,
        "security_protocol": "SASL_SSL",
        "sasl_mechanism": "SCRAM-SHA-512",
        "api_version": (3, 5, 1),
        "sasl_plain_username": keys["username"],
        "sasl_plain_password": keys["password"],
    }
    conf.update(extra_configs)
    return conf


class KafkaAdmin(KafkaAdminClient):
    def __init__(self, **configs):
        if not kafka_available:
            warnings.warn(
                "kafka-python is not installed. Kafka functionality will not be available.", UserWarning)
            return
        super().__init__(**get_diaspora_config(configs))


class KafkaProducer(KafkaProducer):
    def __init__(self, **configs):
        if not kafka_available:
            warnings.warn(
                "kafka-python is not installed. Kafka functionality will not be available.", UserWarning)
            return
        configs.setdefault("value_serializer",
                           lambda v: json.dumps(v).encode('utf-8'))
        super().__init__(**get_diaspora_config(configs))


class KafkaConsumer(KafkaConsumer):
    def __init__(self, *topics, **configs):
        if not kafka_available:
            warnings.warn(
                "kafka-python is not installed. Kafka functionality will not be available.", UserWarning)
            return
        super().__init__(*topics, **get_diaspora_config(configs))
