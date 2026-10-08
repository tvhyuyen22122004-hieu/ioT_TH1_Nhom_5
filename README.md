# Thực hành Python với giao thức MQTT

## Thông tin nhóm

- Trần Văn Hiếu – B23DCCN313
- Nguyễn Viết Tỉnh – B23DCCN825

**Nhóm thực hiện**

| Mã sinh viên | Họ tên |
|---|---|
| B23DCCN313 | Trần Văn Hiếu |
| B23DCCN825 | Nguyễn Viết Tỉnh |

## 1. Chuẩn bị

- Python 3.x
- Thư viện `paho-mqtt`:

```bash
python -m pip install "paho-mqtt>=1.6,<3"
```

## 2. Cấu hình MQTT broker

Bài này dùng broker công khai **HiveMQ**: `broker.hivemq.com`, cổng `1883`. Không cần cài hay chạy Mosquitto.

> Đây là broker dùng chung. Bài 1 gửi tên và mã sinh viên lên broker theo yêu cầu bài tập; không gửi thêm mật khẩu, thông tin tài khoản hoặc dữ liệu riêng tư khác.

Có thể đổi broker bằng biến môi trường (đọc trong `mqtt_config.py`):

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `MQTT_HOST` | `broker.hivemq.com` | Địa chỉ broker |
| `MQTT_PORT` | `1883` | Cổng |
| `MQTT_KEEPALIVE` | `60` | Keepalive (giây) |
| `MQTT_USERNAME` / `MQTT_PASSWORD` | không có | Tài khoản, nếu broker yêu cầu |

Ví dụ dùng Mosquitto cục bộ:

```bash
# Linux / macOS
MQTT_HOST=localhost python subscriber_bai1.py
# Windows PowerShell
$env:MQTT_HOST="localhost"; python subscriber_bai1.py
```

## 3. Cách chạy

Mỗi bài cần **hai terminal riêng**. Chạy subscriber/device **trước**, publisher/controller **sau**.

### Bài 1 – Gửi và nhận thông điệp cơ bản

Topic: `iot/lab/message`

```bash
# Terminal 1
python subscriber_bai1.py
# Terminal 2
python publisher_bai1.py
```

- Publisher cho nhập lời chào, có thể gửi nhiều lần; nhập `EXIT` để kết thúc. Payload gồm lời chào, mã sinh viên và họ tên.
- Subscriber chạy liên tục, in Topic, Payload và Time; nhấn `Ctrl+C` để dừng.

### Bài 2 – Mô phỏng cảm biến nhiệt độ, độ ẩm

Topic: `iot/lab/sensor01/data`

```bash
# Terminal 1
python monitor_subscriber_bai2.py
# Terminal 2
python sensor_publisher_bai2.py
```

- Sensor gửi JSON mỗi 3 giây, ví dụ `{"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}`.
- Monitor in dữ liệu và cảnh báo:
  - `CANH BAO: Nhiet do cao` khi nhiệt độ > 35 °C
  - `CANH BAO: Do am thap` khi độ ẩm < 40 %

### Bài 3 – Điều khiển đèn thông minh

Topic lệnh: `iot/lab/light01/cmd` · Topic trạng thái: `iot/lab/light01/status`

```bash
# Terminal 1
python device_bai3.py
# Terminal 2
python controller_bai3.py
```

- Nhập `ON` hoặc `OFF` ở controller để gửi lệnh; device đổi trạng thái rồi publish `{"device_id": "light01", "status": "ON"}`.
- Lệnh sai sẽ báo lỗi; nhập `EXIT` hoặc `Ctrl+C` để thoát.

## 4. Cấu trúc thư mục

| File | Mô tả |
|---|---|
| `mqtt_config.py` | Cấu hình và hàm kết nối broker dùng chung |
| `publisher_bai1.py`, `subscriber_bai1.py` | Bài 1 |
| `sensor_publisher_bai2.py`, `monitor_subscriber_bai2.py` | Bài 2 |
| `device_bai3.py`, `controller_bai3.py` | Bài 3 |

## 5. Kết quả đạt được

- [x] Bài 1: kết nối broker, publish/subscribe đúng topic, hiển thị Topic/Payload/Time; hỗ trợ gửi nhiều thông điệp và chạy liên tục.
- [x] Bài 2: gửi JSON định kỳ 3 giây, subscriber phân tích dữ liệu và cảnh báo đúng ngưỡng.
- [x] Bài 3: điều khiển hai chiều qua MQTT, thiết bị phản hồi trạng thái; xử lý lệnh sai và lệnh `EXIT`.
