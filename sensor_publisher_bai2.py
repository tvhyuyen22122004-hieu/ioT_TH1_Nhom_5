"""Bài 2: mô phỏng sensor gửi nhiệt độ và độ ẩm mỗi 3 giây."""

import json
import random
import time

from mqtt_config import connect, create_client


TOPIC = "iot/lab/sensor01/data"


def main() -> None:
    client = create_client("python-lab-sensor01")
    try:
        connect(client)
        client.loop_start()
        print(f"Đã kết nối MQTT. Gửi dữ liệu mỗi 3 giây lên {TOPIC}; Ctrl+C để dừng.")
        while True:
            reading = {
                "device_id": "sensor01",
                "temperature": round(random.uniform(20.0, 40.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1),
            }
            payload = json.dumps(reading, ensure_ascii=False)
            client.publish(TOPIC, payload, qos=1)
            print(f"Đã gửi: {payload}")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nĐã dừng sensor publisher.")
    except OSError as exc:
        print(f"Lỗi MQTT: {exc}")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
