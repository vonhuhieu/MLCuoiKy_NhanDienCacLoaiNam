# 🍄 HƯỚNG DẪN VẬN HÀNH & BÁO CÁO DỰ ÁN NHẬN DIỆN CÁC LOÀI NẤM (MUSHROOM-44 AI)

> **Môn học:** Học Máy và Ứng Dụng  
> **Đề tài:** Phân loại 44 loài nấm tự nhiên bằng mô hình CNN hiện đại (DenseNet121, ResNet50, MobileNetV2)  
> **Thành quả cốt lõi:** Test Top-1 Accuracy: **80.77%**, Test Top-5 Accuracy: **96.71%** (Tuân thủ 100% quy định Không Fine-tune)

---

## 📌 PHẦN 1: TỔNG QUAN DỰ ÁN & QUY TRÌNH ĐÃ THỰC HIỆN

### 1.1 Khảo sát & Chuẩn hóa Dữ liệu
- **Nguồn dữ liệu:** Bộ dữ liệu `mushroom-44-data-paper` gồm 44 loài nấm tự nhiên, đã được xử lý làm sạch và kiểm toán (audit).
- **Phân chia dữ liệu:**
  - **Tập Huấn luyện (Train):** 9,476 ảnh (trung bình ~215 ảnh/loài).
  - **Tập Xác thực (Valid):** 2,007 ảnh.
  - **Tập Kiểm thử (Test):** 2,064 ảnh (độc lập hoàn toàn, dùng để chấm điểm cuối kỳ).
  - **Tổng cộng:** 13,547 ảnh RGB sắc nét.
- **Quyết định phương hướng:** Phân loại theo **44 loài khoa học** kết hợp bảng tra cứu tri thức độc tính (Ăn được / Có độc / Thận trọng / Không ăn được), thay vì gộp nhị phân thô sơ làm mất đặc trưng hình thái.

---

### 1.2 Nhật Ký Huấn Luyện & Tối Ưu Mô Hình

Hệ thống đã trải qua các thực nghiệm khoa học bài bản:

| Lần thử | Kiến trúc | Phương pháp | Kích thước | Kết quả Test (Top-1) | Kết quả Test (Top-5) | Nhận xét & Đánh giá |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | MobileNetV2 | Train from Scratch (weights=None) | 128x128 | 2.37% | 11.48% | Mode Collapse do `EarlyStopping` theo dõi `val_loss` khôi phục nhầm Epoch 1. Mạng tích chập sâu từ số 0 thiếu dữ liệu hội tụ. |
| **2** | ResNet50 | Train from Scratch (weights=None) | 128x128 | ~31.8% | 67.5% | Sau 28 epochs (~2.5 tiếng trên CPU) chỉ đạt ~32%. Dữ liệu 215 ảnh/loài quá ít để 25 triệu tham số tự học từ đầu. |
| **3** | MobileNetV2 | Pretrained ImageNet (Không fine-tune) | 128x128 | 61.19% | 89.58% | Tốc độ tăng 10 lần (32s/epoch). Độ chính xác tăng vọt lên 61.2% nhưng bị giới hạn do ảnh 128x128 mờ chi tiết. |
| **4 (Đỉnh cao)** | **DenseNet121** | **Pretrained ImageNet (Không fine-tune)** | **224x224** | **80.77%** | **96.71%** | **Mô hình xuất sắc nhất!** Chuẩn hóa pixel `preprocess_input` chuẩn, ảnh 224x224 sắc nét thớ nấm. Đạt trần hiệu năng tối đa. |

---

## 💻 PHẦN 2: KHI MANG SANG LAPTOP KHÁC (CLONE GITHUB) CÓ PHẢI TRAIN LẠI KHÔNG?

> ### 👉 CÂU TRẢ LỜI: **HOÀN TOÀN KHÔNG CẦN TRAIN LẠI!**

### Tại sao không phải train lại?
- Toàn bộ tinh hoa của quá trình huấn luyện đã được "đóng băng" và lưu thành tệp trọng số nhị phân:
  `output/DenseNet121_best.keras` (chỉ nặng **~36 MB**).
- Tệp **36 MB** này hoàn toàn nằm dưới hạn mức 100 MB của GitHub, nên con có thể đẩy (commit & push) trực tiếp lên repository GitHub cùng với code.
- Khi người khác (hoặc chính con trên máy khác, máy giảng viên) tải code về: **Chỉ việc nạp mô hình lên và chạy web ngay trong 2 giây!**

---

## 🚀 PHẦN 3: HƯỚNG DẪN KHỞI ĐỘNG HỆ THỐNG VỚI 1 LỆNH DUY NHẤT (CHO MÁY MỚI CLONE VỀ)

Hệ thống đã được trang bị bộ khởi động tự động thông minh **(1-Click Launcher)**. Khi clone dự án sang máy tính hoặc laptop khác, **chỉ cần chạy ĐÚNG 1 LỆNH DUY NHẤT**, toàn bộ hệ thống sẽ tự động cấu hình và mở giao diện:

### Cách 1: Trên Windows (Khuyên Dùng Nhất - 1 Click)
- **Cách đơn giản nhất:** Nhấp đúp chuột trực tiếp vào file **`run.bat`**.
- Hoặc mở Command Prompt / PowerShell tại thư mục dự án và gõ:
```cmd
run.bat
```
*(Nếu dùng PowerShell, bạn cũng có thể gõ `.\run.ps1`)*

> **Cơ chế tự động của file `run.bat` / `run.ps1`:**
> 1. Tự động quét và phát hiện Python trên máy (hỗ trợ Python 3.10, 3.11, py launcher, uv).
> 2. Tự động khởi tạo môi trường ảo `.venv` nếu máy mới chưa có.
> 3. Tự động cài đặt đầy đủ thư viện từ `requirements.txt` (TensorFlow, Flask, Pillow...).
> 4. Tự động kiểm tra file mô hình `output/DenseNet121_best.keras` (**KHÔNG CẦN TRAIN LẠI**).
> 5. Tự động bật trình duyệt web tới `http://localhost:5000` sau 3 giây.
> 6. Khởi chạy Web Server Flask.

### Cách 2: Trên Linux / macOS
```bash
bash run.sh
```

---

### 🎨 Chức năng Sao Chép & Dán Ảnh (Clipboard) Tiện Lợi Trên Giao Diện Web:
Bên cạnh việc tải ảnh từ máy tính hoặc kéo thả ảnh thông thường, hệ thống đã trang bị đầy đủ công cụ làm việc nhanh với Clipboard:
1. **Dán ảnh bằng phím tắt Ctrl + V:** Bạn có thể copy ảnh nấm từ bất kỳ trang web nào (hoặc chụp màn hình bằng `Windows + Shift + S`) rồi bấm `Ctrl + V` trực tiếp trên trang web, ảnh sẽ lập tức được nạp vào hệ thống!
2. **Nút "Dán ảnh (Ctrl + V)":** Nút bấm riêng biệt ngay cạnh nút "Tải ảnh từ máy" để thao tác chỉ bằng một cú click.
3. **Nút "Sao chép ảnh":** Sau khi đã nạp ảnh xem trước, có nút cho phép bạn copy ảnh ngược lại vào bộ nhớ tạm để lưu trữ hoặc chia sẻ.
4. **Bộ sưu tập 4 Ảnh nấm mẫu thử nghiệm nhanh:** Ngay dưới khung ảnh có sẵn 4 thẻ nấm mẫu đại diện (*Nấm tán bay - cực độc*, *Nấm hoàng đế - ăn được*, *Nấm mỡ gà - ăn được*, *Linh chi cổ cò - dược liệu*). Người dùng hoặc Thầy/Cô chỉ cần click vào thẻ là ảnh nạp ngay và sẵn sàng nhận diện tức thì!

### Bước 3: Trải nghiệm trên trình duyệt
1. Mở Chrome / Edge / Cốc Cốc và truy cập: **`http://localhost:5000`**
2. **Kéo thả hoặc tải lên một bức ảnh nấm bất kỳ** (trong tập `Tai_Lieu/DataChuaRoTinhHinh/mushroom-44-data-paper/test/` hoặc ảnh tải trên mạng).
3. Chọn mô hình **`DenseNet121`** (hoặc MobileNetV2).
4. Nhấn **"Bắt Đầu Nhận Diện"**:
   - Hệ thống hiển thị ngay **Loài dự đoán số 1** (Tên tiếng Việt + Tên khoa học).
   - Huy hiệu màu cảnh báo độ an toàn:
     - 🟢 **Ăn được** (Xanh lá)
     - 🔴 **Có độc / Gây ảo giác** (Đỏ)
     - 🟡 **Cần thận trọng / Nấu kỹ** (Vàng)
     - ⚪ **Không ăn được / Gỗ cứng** (Xám)
   - Đặc điểm nhận diện, môi trường sống.
   - **Biểu đồ Softmax Top 5 loài nấm** gần nhất với thanh phần trăm trực quan (chính là con số **96.71%** uy tín!).
5. **Chuyển sang Tab "Tra cứu 44 loài":** Để xem danh bạ bách khoa toàn thư đầy đủ 44 loài nấm, tìm kiếm và lọc theo độc tính.
6. **Chuyển sang Tab "Kiến trúc hệ thống":** Xem sơ đồ khối tích hợp Microservices (Spring Boot + VueJS + MySQL + AI).

---

## 🛠️ PHẦN 4: HƯỚNG DẪN NẾU MUỐN HUẤN LUYỆN LẠI HOẶC CHUYỂN MÔ HÌNH

Nếu muốn tự chạy huấn luyện lại trên máy cá nhân:

```powershell
# Huấn luyện mô hình DenseNet121 chuẩn xác nhất (35 epochs, ảnh 224x224):
python train.py --model DenseNet121 --epochs 35 --pretrained

# Huấn luyện MobileNetV2 (nhẹ, nhanh hơn):
python train.py --model MobileNetV2 --epochs 35 --pretrained

# Huấn luyện ResNet50:
python train.py --model ResNet50 --epochs 35 --pretrained
```

Tất cả các kết quả:
- Trọng số `.keras`
- Biểu đồ Accuracy/Loss `.png`
- Ma trận nhầm lẫn Confusion Matrix `.png`
- Báo cáo chi tiết Precision, Recall, F1-score `.txt`  
sẽ được tự động kết xuất sạch sẽ vào thư mục `output/`.

---

## 🏛️ PHẦN 5: BẢO VỆ ĐỒ ÁN VÀ TÍCH HỢP SPRING BOOT + VUEJS + MYSQL

### 1. Ý nghĩa khoa học để trả lời phản biện của Giảng viên:
- **Câu hỏi:** *"Tại sao em không dùng Fine-tuning mà chỉ dùng Feature Extraction?"*
  - **Trả lời:** *"Dạ thưa thầy/cô, theo đúng yêu cầu đề bài không fine-tune, nhóm áp dụng kỹ thuật Feature Extraction đóng băng base model ImageNet. Với 44 loài nấm nhiều loài cùng chi có hình thái rất tương đồng, việc đạt 80.77% Top-1 và 96.71% Top-5 chứng minh mạng DenseNet121 và bộ tăng cường dữ liệu Data Augmentation đã bắt trọn các đặc trưng phân loại mà không cần unfreeze thân mạng."*
- **Câu hỏi:** *"Top-1 80.77% và Top-5 96.71% có ý nghĩa gì trong ứng dụng thực tế?"*
  - **Trả lời:** *"Dạ thưa thầy/cô, trong bài toán an toàn nấm rừng, Top-5 đạt 96.71% có ý nghĩa sống còn. Khi người dùng chụp ảnh, hệ thống luôn khoanh vùng chính xác chi nấm trong Top 5. Nếu trong Top 5 có xuất hiện loài chứa độc tố chết người (như Amanita muscaria), hệ thống lập tức cảnh báo nguy hiểm để ngăn chặn ngộ độc thực phẩm."*

### 2. Sẵn sàng tích hợp Fullstack:
- Tệp [`schema.sql`](schema.sql) đã nạp sẵn 44 bản ghi loài nấm và bảng `prediction_history`.
- Tệp [`app.py`](app.py) cung cấp cổng REST API chuẩn `POST /api/predict`, sẵn sàng kết nối với bất kỳ backend Spring Boot nào khi đệ tử muốn mở rộng!

