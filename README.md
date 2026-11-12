# 🍄 Đồ Án Cuối Kỳ: Nhận Diện Các Loài Nấm (Mushroom-44 Classification)

> **Môn học:** Học Máy và Ứng Dụng  
> **Kiến trúc mạng:** CNN Hiện Đại (ResNet50, DenseNet121, MobileNetV2)  
> **Đặc điểm huấn luyện:** Train from scratch (weights=None, không fine-tune), Data Augmentation, phân loại đa lớp (44 classes, Softmax Output)  
> **Ứng dụng:** Web App nhận diện trực quan + Hỗ trợ kiến trúc Doanh nghiệp (Spring Boot + VueJS + MySQL)

---

## 📂 1. Cấu Trúc Dự Án

```
CuoiKy_NhanDienCacLoaiNam/
├── train.py                     # Script huấn luyện CNN (ResNet, DenseNet, MobileNet)
├── mushroom_info.py             # Tri thức 44 loài nấm (tên VN, độc tính, mô tả)
├── app.py                       # REST API & Web Server (Flask)
├── schema.sql                   # CSDL MySQL (44 loài + bảng lịch sử nhận diện)
├── requirements.txt             # Danh sách thư viện Python cần thiết
├── templates/
│   └── index.html               # Giao diện Web SPA tích hợp Vue 3 + TailwindCSS
├── output/                      # Thư mục lưu kết quả sau khi train
│   ├── class_names.json         # Danh sách 44 lớp sắp xếp theo index
│   ├── {Model}_best.keras       # File trọng số mô hình tốt nhất
│   ├── {Model}_history.png      # Đồ thị Accuracy & Loss
│   ├── {Model}_confusion_matrix.png # Ma trận nhầm lẫn
│   └── {Model}_report.txt       # Báo cáo Precision, Recall, F1-score
└── Tai_Lieu/
    ├── DataHienTai/             # Báo cáo audit dữ liệu & dedup
    └── DataChuaRoTinhHinh/      # Dataset ảnh gốc 44 loài nấm (train/valid/test)
        └── mushroom-44-data-paper/
            ├── train/           (9,476 ảnh)
            ├── valid/           (2,007 ảnh)
            └── test/            (2,064 ảnh)
```

---

## 🚀 2. Khởi Động Nhanh Với 1 Lệnh Duy Nhất (1-Click Launcher)

> **💡 LƯU Ý QUAN TRỌNG:** Sau khi clone mã nguồn về, bạn **HOÀN TOÀN KHÔNG CẦN TRAIN LẠI!** Mô hình đỉnh cao `DenseNet121` (Đạt độ chính xác Top-1: **80.77%**, Top-5: **96.71%**) đã được huấn luyện sẵn và lưu tại `output/DenseNet121_best.keras`.

Chỉ cần chạy **ĐÚNG 1 LỆNH**:

- **Trên Windows (Nhấp đúp chuột hoặc CMD):**
  ```cmd
  run.bat
  ```
  *(Hoặc chạy `.\run.ps1` trong PowerShell)*

- **Trên Linux / macOS:**
  ```bash
  bash run.sh
  ```

*Script khởi động sẽ tự động tạo môi trường ảo `.venv`, cài đặt thư viện cần thiết, tự động bật trình duyệt `http://localhost:5000` và khởi chạy web server.*

---

## 🎨 3. Tính Năng Sao Chép & Dán Ảnh (Clipboard) Tiện Lợi

- **Dán ảnh mọi lúc bằng phím tắt:** Nhấn phím <kbd>Ctrl + V</kbd> ở bất kỳ đâu trên trang web để dán ngay bức ảnh nấm bạn vừa copy trên mạng hoặc chụp màn hình.
- **Nút "Dán ảnh (Ctrl + V)":** Nút bấm riêng biệt ngay cạnh nút "Tải ảnh từ máy" để thao tác chỉ bằng 1 click.
- **Nút "Sao chép ảnh":** Cho phép copy bức ảnh đang hiển thị vào clipboard máy tính.
- **Bộ 4 ảnh nấm mẫu thử nhanh:** Chọn nhanh các loài nấm đặc trưng (*Amanita muscaria*, *Agaricus augustus*, *Cantharellus californicus*, *Ganoderma applanatum*) để kiểm thử ngay lập tức.

---

## 🏋️ 4. Hướng Dẫn Nếu Muốn Tự Huấn Luyện Lại (Tùy Chọn)

Sau khi có mô hình, khởi chạy server:

```bash
python app.py
```

Mở trình duyệt truy cập: **`http://localhost:5000`**

### Các tính năng chính:
1. **Nhận Diện Ảnh:** Kéo thả ảnh nấm, chọn mô hình (MobileNetV2 / ResNet50 / DenseNet121), nhấn "Nhận Diện".
2. **Cảnh Báo Độc Tính:** Huy hiệu cảnh báo rõ ràng:
   - 🟢 **Ăn được:** An toàn để chế biến
   - 🔴 **Có độc:** Chứa độc tố thần kinh, tổn thương gan hoặc gây ảo giác
   - 🟡 **Cần cẩn trọng:** Cần nấu chín kỹ hoặc dễ dị ứng
   - ⚪ **Không ăn được:** Thịt gỗ cứng dai, thịt mỏng hoặc vị rất đắng
3. **Softmax Probabilities:** Hiển thị biểu đồ xác suất Top 5 loài nấm gần nhất (tổng 44 lớp bằng 1).
4. **Bách Khoa 44 Loài Nấm:** Tra cứu nhanh đặc điểm, môi trường sống, độc tính của từng loài.

---

## 🏛️ 4. Tích Hợp Kiến Trúc Spring Boot + VueJS + MySQL

Đồ án hoàn toàn hỗ trợ tích hợp với hệ sinh thái **Spring Boot + VueJS + MySQL** theo mô hình Microservices:

```
[ VueJS Frontend ] (Port 3000 / 5173)
       │  (HTTP / REST)
       ▼
[ Spring Boot API ] (Port 8080)  ◄──────►  [ MySQL Database ] (mushroom_db)
       │  (Multipart POST /api/predict)
       ▼
[ Python AI Service (app.py) ] (Port 5000)
```

1. **Khởi tạo MySQL Database:**
   Chạy script `schema.sql` vào MySQL để tạo database `mushroom_db`, nạp sẵn dữ liệu bách khoa 44 loài và bảng `prediction_history`.
2. **Spring Boot:** Tạo REST Controller nhận ảnh tải lên từ VueJS, chuyển tiếp sang `http://localhost:5000/api/predict` bằng `RestTemplate` hoặc `WebClient`, lưu kết quả vào MySQL rồi trả về cho VueJS.
3. **VueJS:** Xây dựng giao diện tải ảnh, xem lịch sử các lần nhận diện đã lưu trong database.
