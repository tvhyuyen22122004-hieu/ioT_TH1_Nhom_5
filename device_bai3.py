"""Bài 3: thiết bị đèn nhận lệnh và publish trạng thái."""

import json

from mqtt_config import connect, create_client


COMMAND_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"
status = "OFF"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Đã kết nối MQTT. Đang chờ lệnh tại {COMMAND_TOPIC}")
        client.subscribe(COMMAND_TOPIC, qos=1)
    else:
        print(f"Không thể kết nối MQTT, mã lỗi: {reason_code}")


def on_message(client, userdata, message):
    global status
    command = message.payload.decode("utf-8", errors="replace").strip().upper()
    if command not in {"ON", "OFF"}:
        print(f"Lệnh không hợp lệ: {command}")
        return

    status = command
    payload = json.dumps({"device_id": "light01", "status": status})
    client.publish(STATUS_TOPIC, payload, qos=1)
    print(f"Nhận lệnh {command}; đã cập nhật trạng thái đèn.")


def main() -> None:
    client = create_client("python-lab-light01")
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
