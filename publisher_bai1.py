"""Bài 1: publish lời chào lên topic iot/lab/message."""

from mqtt_config import connect, create_client


TOPIC = "iot/lab/message"


def main() -> None:
    students = "B23DCCN313 - Trần Văn Hiếu; B23DCCN825 - Nguyễn Viết Tỉnh"
    client = create_client("python-lab-bai1-publisher")
    try:
        connect(client)
        client.loop_start()
        print(f"Đã kết nối MQTT. Topic: {TOPIC}")
        print("Nhập lời chào; nhập EXIT để kết thúc.")
        while True:
            greeting = input("Nội dung: ").strip()
            if greeting.upper() == "EXIT":
                break
            if not greeting:
                continue
            payload = f"{greeting} - {students}"
            info = client.publish(TOPIC, payload, qos=1)
            info.wait_for_publish()
            print(f"Đã gửi: {payload}")
    except (OSError, KeyboardInterrupt) as exc:
        if isinstance(exc, OSError):
            print(f"Lỗi MQTT: {exc}")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
