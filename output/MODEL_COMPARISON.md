# 📊 BẢNG SO SÁNH CHI TIẾT HIỆU NĂNG 3 MÔ HÌNH CNN (MUSHROOM-44 AI)

> **Bộ dữ liệu kiểm thử (Test Set):** 2,064 ảnh độc lập thuộc 44 loài nấm tự nhiên  
> **Quy định nghiêm ngặt:** Tuân thủ 100% yêu cầu đề bài **KHÔNG FINE-TUNE** (Feature Extraction với Frozen Backbone hoặc Train from Scratch)

---

## 1. BẢNG TỔNG HỢP SO SÁNH ĐỐI ĐẦU

| Tiêu chí đánh giá | DenseNet121 *(Pretrained)* | MobileNetV2 *(Pretrained)* | ResNet50 *(From Scratch)* |
|:---|:---:|:---:|:---:|
| **Phương pháp huấn luyện** | Feature Extraction (Frozen Base) | Feature Extraction (Frozen Base) | Train from Scratch (Khởi tạo ngẫu nhiên) |
| **Kích thước ảnh đầu vào** | **224 x 224 x 3** | 128 x 128 x 3 | 128 x 128 x 3 |
| **Số lượng tham số (Params)** | ~8.0 Triệu | **~3.5 Triệu (Nhẹ nhất)** | ~25.6 Triệu (Nặng nhất) |
| **Dung lượng file Model** | **34.6 MB** | **18.4 MB** | 284.0 MB |
| **Thời gian train / epoch** | ~40 giây | **~25 giây (Nhanh nhất)** | ~260 giây (Rất chậm) |
| **Test Loss** | **0.7387** | 1.3421 | 2.4302 |
| **Test Top-1 Accuracy** | **80.77% 🏆** | 61.19% | 30.67% |
| **Test Top-5 Accuracy** | **96.71% 🏆** | 89.58% | 66.42% |
| **Xếp hạng & Ứng dụng** | **Mô hình xuất sắc nhất** (Mặc định) | Mô hình siêu nhẹ (Phù hợp Mobile/IoT) | Kém hiệu quả (Minh chứng thiếu dữ liệu) |

---

## 2. PHÂN TÍCH CHUYÊN SÂU TỪNG MÔ HÌNH

### 🥇 1. DenseNet121 (Dense Convolutional Network) - QUÁN QUÂN
- **Kết quả:** Top-1: **80.77%** | Top-5: **96.71%** | Loss: **0.7387**
- **Tại sao vượt trội?**
  - Cơ chế **Dense Connectivity** (kết nối dày đặc): Mỗi tầng nhận feature map từ tất cả các tầng trước đó, giúp tái sử dụng đặc trưng tối đa và giảm thiểu triệt để hiện tượng tiêu biến gradient.
  - Kích thước ảnh 224x224 giữ nguyên độ sắc nét của các vi đặc trưng nấm (vân vảy mũ nấm, vòng cổ, thớ thịt cuống nấm).
  - Chuẩn hóa đầu vào `tf.keras.applications.densenet.preprocess_input` khớp chuẩn với phân phối ImageNet.
- **Tập tin báo cáo:**
  - Báo cáo chi tiết: `output/DenseNet121_pretrained_report.txt`
  - Ma trận nhầm lẫn: `output/DenseNet121_pretrained_confusion_matrix.png`
  - Đồ thị huấn luyện: `output/DenseNet121_pretrained_history.png`

---

### 🥈 2. MobileNetV2 (Inverted Residuals & Linear Bottlenecks) - Á QUÂN
- **Kết quả:** Top-1: **61.19%** | Top-5: **89.58%** | Loss: **1.3421**
- **Đặc tính:**
  - Tối ưu hóa cực đại về tốc độ và bộ nhớ (chỉ 3.5 triệu tham số, file model 18.4 MB).
  - Tốc độ suy luận chỉ mất **~0.15 giây/ảnh**, cực kỳ thích hợp cho các thiết bị di động hoặc máy tính cấu hình yếu.
  - Điểm hạn chế: Do huấn luyện ở kích thước 128x128 để tối ưu tốc độ, một số đặc trưng nấm tinh vi bị mờ dẫn đến độ chính xác Top-1 đạt 61.2% (tuy nhiên Top-5 vẫn rất cao: 89.58%).
- **Tập tin báo cáo:**
  - Báo cáo chi tiết: `output/MobileNetV2_pretrained_report.txt`
  - Ma trận nhầm lẫn: `output/MobileNetV2_pretrained_confusion_matrix.png`
  - Đồ thị huấn luyện: `output/MobileNetV2_pretrained_history.png`

---

### 🥉 3. ResNet50 (Residual Network) - ĐỐI CHỨNG (FROM SCRATCH)
- **Kết quả:** Top-1: **30.67%** | Top-5: **66.42%** | Loss: **2.4302**
- **Đặc tính & Bài học khoa học rút ra:**
  - ResNet50 có tới 25.6 triệu tham số. Khi huấn luyện hoàn toàn từ số 0 (weights=None) trên tập dữ liệu chỉ có ~215 ảnh/loài nấm, mô hình bị **thiếu hụt dữ liệu trầm trọng**.
  - Không thể tự học được các bộ lọc không gian (Gabor filters, edge detectors, texture filters) vốn cần hàng triệu ảnh ImageNet.
  - Thời gian huấn luyện rất lâu (gấp 8-10 lần các mạng khác) nhưng độ chính xác chỉ dừng ở ~30.67%. Đây là minh chứng khoa học đắt giá trong báo cáo để chứng minh giá trị của **Transfer Learning / Pretrained Feature Extraction**.
- **Tập tin báo cáo:**
  - Báo cáo chi tiết: `output/ResNet50_report.txt`
  - Ma trận nhầm lẫn: `output/ResNet50_confusion_matrix.png`

---

## 3. KẾT LUẬN & KIẾN NGHỊ BẢO VỆ ĐỒ ÁN
1. **Lựa chọn mô hình đưa vào sản phẩm thực tế:** Chọn **DenseNet121** làm mô hình mặc định trên Web/App vì đạt độ chính xác Top-5 lên tới **96.71%**, thời gian phản hồi nhanh và kích thước file chỉ 34.6MB.
2. **Giá trị học thuật:** Đã thực hiện đầy đủ ma trận thực nghiệm so sánh đa dạng (DenseNet vs ResNet vs MobileNet), giải thích thấu đáo tại sao một số mô hình đạt 80% còn mô hình từ đầu chỉ đạt 30%.

