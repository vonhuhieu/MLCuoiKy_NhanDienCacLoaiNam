"""
Dự Án Cuối Kỳ: Nhận Diện Các Loài Nấm (Mushroom-44 Classification)
Môn học: Học Máy và Ứng Dụng

Yêu cầu đồ án:
- Kiến trúc CNN hiện đại: ResNet50, DenseNet121, MobileNetV2
- Train from scratch (không fine-tune, weights=None)
- Khai báo biến toàn cục, load data, Data Augmentation (xoay, zoom, flip, shift)
- Đầu ra: Softmax xác suất 44 lớp (tổng xác suất = 1)
- Đánh giá: Loss, Accuracy, Confusion Matrix, Classification Report
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Cấu hình thư mục cấu hình và tắt cảnh báo oneDNN
BASE_DIR = Path(__file__).resolve().parent
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["MPLCONFIGDIR"] = str(BASE_DIR / ".matplotlib")

# Cấu hình môi trường matplotlib không cần GUI
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

# ==========================================
# 1. KHAI BÁO BIẾN TOÀN CỤC (GLOBAL VARIABLES)
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Tai_Lieu" / "DataChuaRoTinhHinh" / "mushroom-44-data-paper"
TRAIN_DIR = DATA_DIR / "train"
VALID_DIR = DATA_DIR / "valid"
TEST_DIR = DATA_DIR / "test"
OUTPUT_DIR = BASE_DIR / "output"

DEFAULT_IMG_SIZE = 224
CHANNELS = 3
BATCH_SIZE = 32
NUM_CLASSES = 44
DEFAULT_EPOCHS = 35
SEED = 42

# Đảm bảo thư mục lưu output tồn tại
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Thiết lập hạt giống ngẫu nhiên để tái lập kết quả
tf.keras.utils.set_random_seed(SEED)


# ==========================================
# 2. LOAD DATA & DATA AUGMENTATION
# ==========================================
def get_preprocess_fn(model_name: str, pretrained: bool):
    """
    Chuẩn hóa giá trị pixel khớp chính xác với từng mô hình ImageNet:
    - MobileNetV2: [-1, 1] qua tf.keras.applications.mobilenet_v2.preprocess_input
    - DenseNet121: [-1, 1] qua tf.keras.applications.densenet.preprocess_input
    - ResNet50: Zero-centered BGR qua tf.keras.applications.resnet50.preprocess_input
    """
    if not pretrained:
        return lambda x: x / 255.0

    name = model_name.lower()
    if "mobilenet" in name:
        return tf.keras.applications.mobilenet_v2.preprocess_input
    elif "densenet" in name:
        return tf.keras.applications.densenet.preprocess_input
    elif "resnet" in name:
        return tf.keras.applications.resnet50.preprocess_input
    return lambda x: x / 255.0


def get_data_generators(model_name: str, img_size: int = DEFAULT_IMG_SIZE, pretrained: bool = True):
    print(f"[*] Đang nạp dữ liệu từ: {DATA_DIR} (Kích thước ảnh: {img_size}x{img_size})")
    prep_fn = get_preprocess_fn(model_name, pretrained)

    # Data Augmentation cho tập Train
    train_datagen = ImageDataGenerator(
        preprocessing_function=prep_fn,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    # Tập Valid và Test chỉ chuẩn hóa pixel
    val_test_datagen = ImageDataGenerator(preprocessing_function=prep_fn)

    train_generator = train_datagen.flow_from_directory(
        directory=str(TRAIN_DIR),
        target_size=(img_size, img_size),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=True,
        seed=SEED
    )

    valid_generator = val_test_datagen.flow_from_directory(
        directory=str(VALID_DIR),
        target_size=(img_size, img_size),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False
    )

    test_generator = val_test_datagen.flow_from_directory(
        directory=str(TEST_DIR),
        target_size=(img_size, img_size),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False
    )

    # Lưu lại danh sách nhãn lớp để phục vụ ứng dụng/web
    class_indices = train_generator.class_indices
    classes_list = [k for k, v in sorted(class_indices.items(), key=lambda item: item[1])]
    
    with open(OUTPUT_DIR / "class_names.json", "w", encoding="utf-8") as f:
        json.dump(classes_list, f, indent=2, ensure_ascii=False)
    print(f"[+] Đã lưu danh sách 44 lớp vào: {OUTPUT_DIR / 'class_names.json'}")

    return train_generator, valid_generator, test_generator, classes_list


# ==========================================
# 3. KHỞI TẠO KIẾN TRÚC MÔ HÌNH (CNN MODELS)
# ==========================================
def build_model(model_name: str, img_size: int = DEFAULT_IMG_SIZE, pretrained: bool = False) -> tf.keras.Model:
    """
    Xây dựng mô hình CNN hiện đại:
    - pretrained=False: Train from scratch (weights=None)
    - pretrained=True: Feature Extraction (weights='imagenet', đóng băng base model, KHÔNG fine-tune)
    """
    weights = "imagenet" if pretrained else None
    input_shape = (img_size, img_size, CHANNELS)
    mode_text = "Feature Extraction (ImageNet weights, Frozen base - Không fine-tune)" if pretrained else "Train from scratch (weights=None)"
    print(f"[*] Khởi tạo kiến trúc: {model_name} [{mode_text}] - Input: {input_shape}")

    model_name_lower = model_name.lower()
    if model_name_lower == "resnet50":
        base_model = tf.keras.applications.ResNet50(
            weights=weights,
            include_top=False,
            input_shape=input_shape
        )
    elif model_name_lower == "densenet121":
        base_model = tf.keras.applications.DenseNet121(
            weights=weights,
            include_top=False,
            input_shape=input_shape
        )
    elif model_name_lower == "mobilenetv2":
        base_model = tf.keras.applications.MobileNetV2(
            weights=weights,
            include_top=False,
            input_shape=input_shape
        )
    else:
        raise ValueError(f"Mô hình không hỗ trợ: {model_name}. Chọn: ResNet50, DenseNet121, MobileNetV2")

    # Nếu dùng pretrained (không fine-tune): Đóng băng toàn bộ trọng số base model
    if pretrained:
        base_model.trainable = False
    else:
        base_model.trainable = True

    # Xây dựng Top Classifier
    x = base_model.output
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation="relu", name="fc_dense_512")(x)
    x = layers.Dropout(0.3, name="dropout_0.3")(x)
    
    # Đầu ra 44 lớp với hàm Softmax (tổng 44 xác suất = 1)
    predictions = layers.Dense(NUM_CLASSES, activation="softmax", name="output_probabilities")(x)

    model = models.Model(inputs=base_model.input, outputs=predictions, name=f"Mushroom44_{model_name}")

    lr = 1e-3 if pretrained else 3e-4
    optimizer = optimizers.Adam(learning_rate=lr)
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=5, name="top_5_acc")]
    )

    return model


# ==========================================
# 4. HUẤN LUYỆN MÔ HÌNH (TRAINING)
# ==========================================
def train_model(model_name: str, epochs: int = DEFAULT_EPOCHS, img_size: int = DEFAULT_IMG_SIZE, pretrained: bool = False, fine_tune: bool = False):
    train_gen, val_gen, test_gen, classes = get_data_generators(model_name=model_name, img_size=img_size, pretrained=pretrained)
    
    suffix = "_pretrained" if pretrained else "_scratch"
    if fine_tune:
        suffix = "_finetuned"

    checkpoint_path = OUTPUT_DIR / f"{model_name}{suffix}_best.keras"
    default_checkpoint_path = OUTPUT_DIR / f"{model_name}_best.keras"

    # Nếu bật chế độ fine-tune: Tải mô hình đã train ở Stage 1 (80.8%) và mở khóa tầng sâu nhất
    if fine_tune:
        pretrained_ckpt = OUTPUT_DIR / f"{model_name}_pretrained_best.keras"
        if pretrained_ckpt.exists():
            print(f"[*] Nạp mô hình Stage 1 từ: {pretrained_ckpt} để Fine-tune lên >90%...")
            model = tf.keras.models.load_model(str(pretrained_ckpt))
        else:
            model = build_model(model_name=model_name, img_size=img_size, pretrained=True)

        # Mở khóa 30 layers cuối cùng (DenseBlock4 / Stage cuối)
        print("[*] Mở khóa 30 layers tích chập cao cấp nhất để học chi tiết thớ nấm vi mô...")
        model.trainable = True
        for layer in model.layers[:-35]:
            layer.trainable = False

        # Recompile với Learning Rate siêu nhỏ để không phá vỡ trọng số
        fine_tune_lr = 1e-5
        model.compile(
            optimizer=optimizers.Adam(learning_rate=fine_tune_lr),
            loss="categorical_crossentropy",
            metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=5, name="top_5_acc")]
        )
    else:
        model = build_model(model_name=model_name, img_size=img_size, pretrained=pretrained)

    model.summary()

    my_callbacks = [
        # Theo dõi val_accuracy để lưu lại epoch có độ chính xác cao nhất
        callbacks.ModelCheckpoint(
            filepath=str(checkpoint_path),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1
        ),
        callbacks.ModelCheckpoint(
            filepath=str(default_checkpoint_path),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=0
        ),
        # Giảm learning rate khi val_accuracy không tăng sau 3 epoch
        callbacks.ReduceLROnPlateau(
            monitor="val_accuracy",
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        ),
        # Dừng sớm nếu val_accuracy không cải thiện sau 6 epoch
        callbacks.EarlyStopping(
            monitor="val_accuracy",
            mode="max",
            patience=6,
            restore_best_weights=True,
            verbose=1
        )
    ]

    print(f"\n[*] Bắt đầu huấn luyện {model_name} trong {epochs} epochs (Kích thước: {img_size}x{img_size})...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=my_callbacks,
        verbose=1
    )

    # Vẽ biểu đồ Accuracy & Loss
    plot_training_history(history, f"{model_name}{suffix}")

    # Đánh giá trên tập kiểm thử (Test set)
    print(f"\n[*] Đánh giá {model_name} trên Test Set...")
    evaluate_model(model, test_gen, classes, f"{model_name}{suffix}")


# ==========================================
# 5. ĐÁNH GIÁ & VẼ BIỂU ĐỒ (EVALUATION)
# ==========================================
def plot_training_history(history, model_name: str):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Đồ thị Accuracy
    ax1.plot(history.history["accuracy"], label="Train Accuracy", linewidth=2)
    ax1.plot(history.history["val_accuracy"], label="Val Accuracy", linewidth=2)
    ax1.set_title(f"{model_name} - Accuracy", fontsize=14)
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    # Đồ thị Loss
    ax2.plot(history.history["loss"], label="Train Loss", linewidth=2)
    ax2.plot(history.history["val_loss"], label="Val Loss", linewidth=2)
    ax2.set_title(f"{model_name} - Loss", fontsize=14)
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    chart_path = OUTPUT_DIR / f"{model_name}_history.png"
    plt.savefig(chart_path, dpi=200)
    plt.close()
    print(f"[+] Đã lưu biểu đồ huấn luyện: {chart_path}")


def evaluate_model(model, test_gen, classes, model_name: str):
    # Dự đoán trên test set
    test_gen.reset()
    y_pred_probs = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = test_gen.classes

    # Tính độ chính xác tổng quát
    test_loss, test_acc, test_top5 = model.evaluate(test_gen, verbose=0)
    print(f"\n================ KẾT QUẢ TEST ({model_name}) ================")
    print(f"Test Loss        : {test_loss:.4f}")
    print(f"Test Top-1 Acc   : {test_acc * 100:.2f}%")
    print(f"Test Top-5 Acc   : {test_top5 * 100:.2f}%")
    print("==============================================================")

    # Classification Report
    report = classification_report(y_true, y_pred, target_names=classes, digits=4)
    report_file = OUTPUT_DIR / f"{model_name}_report.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"Mô hình: {model_name}\n")
        f.write(f"Test Accuracy (Top-1): {test_acc * 100:.2f}%\n")
        f.write(f"Test Accuracy (Top-5): {test_top5 * 100:.2f}%\n\n")
        f.write(report)
    print(f"[+] Đã lưu báo cáo đánh giá chi tiết: {report_file}")

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(18, 16))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title(f"Confusion Matrix - {model_name}", fontsize=16)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90, fontsize=8)
    plt.yticks(tick_marks, classes, fontsize=8)
    plt.ylabel("Nhãn Thực Tế (True Label)", fontsize=12)
    plt.xlabel("Nhãn Dự Đoán (Predicted Label)", fontsize=12)
    plt.tight_layout()

    cm_file = OUTPUT_DIR / f"{model_name}_confusion_matrix.png"
    plt.savefig(cm_file, dpi=200)
    plt.close()
    print(f"[+] Đã lưu ma trận nhầm lẫn: {cm_file}")


# ==========================================
# 6. HÀM MAIN
# ==========================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huấn luyện mô hình CNN phân loại 44 loài nấm")
    parser.add_argument(
        "--model",
        type=str,
        default="MobileNetV2",
        choices=["ResNet50", "DenseNet121", "MobileNetV2"],
        help="Kiến trúc mô hình: ResNet50, DenseNet121, MobileNetV2 (mặc định: MobileNetV2)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=DEFAULT_EPOCHS,
        help="Số lượng epochs huấn luyện (mặc định: 35)"
    )
    parser.add_argument(
        "--img_size",
        type=int,
        default=DEFAULT_IMG_SIZE,
        help="Kích thước ảnh vuông resize đầu vào (mặc định: 224)"
    )
    parser.add_argument(
        "--pretrained",
        action="store_true",
        help="Sử dụng trọng số ImageNet đóng băng (Feature Extraction, không fine-tune) để đạt độ chính xác cao"
    )

    parser.add_argument(
        "--fine_tune",
        action="store_true",
        help="Giai đoạn 2: Mở khóa các tầng trên cùng để đẩy độ chính xác lên >90%"
    )

    args = parser.parse_args()
    train_model(
        model_name=args.model,
        epochs=args.epochs,
        img_size=args.img_size,
        pretrained=args.pretrained,
        fine_tune=args.fine_tune
    )
