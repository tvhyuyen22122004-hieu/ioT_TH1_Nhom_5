"""Bài 2: hiển thị dữ liệu cảm biến và cảnh báo vượt ngưỡng."""

import json

from mqtt_config import connect, create_client


TOPIC = "iot/lab/sensor01/data"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Đã kết nối MQTT. Đang lắng nghe {TOPIC}")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Không thể kết nối MQTT, mã lỗi: {reason_code}")


def on_message(client, userdata, message):
    try:
        reading = json.loads(message.payload.decode("utf-8"))
        device_id = reading["device_id"]
        temperature = float(reading["temperature"])
        humidity = float(reading["humidity"])
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Bỏ qua payload không hợp lệ: {exc}")
        return

    print(f"\nDevice: {device_id}")
    print(f"Temperature: {temperature:.1f} C")
    print(f"Humidity: {humidity:.1f} %")
    if temperature > 35:
        print("CANH BAO: Nhiet do cao")
    if humidity < 40:
        print("CANH BAO: Do am thap")


def main() -> None:
    client = create_client("python-lab-monitor")
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
