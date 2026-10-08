"""Shared MQTT connection settings for the lab exercises."""

import os

import paho.mqtt.client as mqtt


def create_client(client_id: str) -> mqtt.Client:
    """Create a client compatible with both paho-mqtt 1.x and 2.x."""
    kwargs = {"client_id": client_id, "clean_session": True}
    if hasattr(mqtt, "CallbackAPIVersion"):
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, **kwargs)
    else:
        client = mqtt.Client(**kwargs)

    username = os.getenv("MQTT_USERNAME")
    password = os.getenv("MQTT_PASSWORD")
    if username:
        client.username_pw_set(username, password)
    return client


def broker_settings() -> tuple[str, int, int]:
    host = os.getenv("MQTT_HOST", "broker.hivemq.com")
    port = int(os.getenv("MQTT_PORT", "1883"))
    keepalive = int(os.getenv("MQTT_KEEPALIVE", "60"))
    return host, port, keepalive


def connect(client: mqtt.Client) -> None:
    host, port, keepalive = broker_settings()
    client.connect(host, port, keepalive)
