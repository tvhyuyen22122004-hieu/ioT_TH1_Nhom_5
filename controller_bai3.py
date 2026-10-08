"""Bài 3: gửi lệnh điều khiển và hiển thị trạng thái đèn."""

import threading

from mqtt_config import connect, create_client


COMMAND_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"
subscribed = threading.Event()


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        client.subscribe(STATUS_TOPIC, qos=1)
    else:
        print(f"Không thể kết nối MQTT, mã lỗi: {reason_code}")


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    subscribed.set()


def on_message(client, userdata, message):
    print("\nTrang thai nhan duoc:")
    print(message.payload.decode("utf-8", errors="replace"))


def main() -> None:
    client = create_client("python-lab-light-controller")
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    try:
        connect(client)
        client.loop_start()
        if not subscribed.wait(timeout=10):
            raise TimeoutError("Chưa đăng ký được topic trạng thái trong 10 giây.")
        print("Đã kết nối và đăng ký topic trạng thái. Nhập ON, OFF hoặc EXIT.")
        while True:
            command = input("Nhap lenh: ").strip().upper()
            if command == "EXIT":
                break
            if command not in {"ON", "OFF"}:
                print("Lệnh không hợp lệ. Chỉ nhập ON, OFF hoặc EXIT.")
                continue
            info = client.publish(COMMAND_TOPIC, command, qos=1)
            info.wait_for_publish()
            print(f"Da gui lenh {command} toi light01")
    except KeyboardInterrupt:
        print("\nĐã dừng controller.")
    except (OSError, TimeoutError) as exc:
        print(f"Lỗi MQTT: {exc}")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
