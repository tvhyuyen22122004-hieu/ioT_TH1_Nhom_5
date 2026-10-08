"""Bài 1: nhận thông điệp trên topic iot/lab/message."""

from datetime import datetime

from mqtt_config import connect, create_client


TOPIC = "iot/lab/message"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Đã kết nối MQTT. Đang lắng nghe {TOPIC}")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Không thể kết nối MQTT, mã lỗi: {reason_code}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8", errors="replace")
    print("\nNhan duoc message:")
    print(f"Topic: {message.topic}")
    print(f"Payload: {payload}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")


def main() -> None:
    client = create_client("python-lab-bai1-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        connect(client)
        client.loop_forever()
    except (OSError, KeyboardInterrupt) as exc:
        if isinstance(exc, OSError):
            print(f"Lỗi MQTT: {exc}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
