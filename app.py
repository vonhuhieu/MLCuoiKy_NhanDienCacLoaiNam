"""
AI Web Service & Demo API: Nhận Diện Các Loài Nấm
Framework: Flask (REST API)
Hỗ trợ:
- Web UI tích hợp VueJS 3 hiện đại
- Cung cấp REST API cho Spring Boot / VueJS / Mobile App
"""

import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["MPLCONFIGDIR"] = str(BASE_DIR / ".matplotlib")

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import numpy as np
import tensorflow as tf

from mushroom_info import MUSHROOM_INFO

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
IMG_SIZE = 128

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR / "static"))
CORS(app)  # Cho phép gọi từ Spring Boot hoặc VueJS chạy trên port khác

# Bộ nhớ đệm lưu trữ các mô hình đã tải
LOADED_MODELS = {}
CURRENT_MODEL_NAME = "DenseNet121"

# Nạp danh sách lớp
CLASS_NAMES = []
class_file = OUTPUT_DIR / "class_names.json"
if class_file.exists():
    with open(class_file, "r", encoding="utf-8") as f:
        CLASS_NAMES = json.load(f)
else:
    # Nếu chưa train, lấy từ MUSHROOM_INFO
    CLASS_NAMES = sorted(list(MUSHROOM_INFO.keys()))


def get_model(model_name: str):
    """Lấy hoặc nạp mô hình từ đĩa vào bộ nhớ."""
    global LOADED_MODELS
    if model_name in LOADED_MODELS:
        return LOADED_MODELS[model_name]

    model_path = OUTPUT_DIR / f"{model_name}_best.keras"
    if not model_path.exists():
        # Tìm các định dạng khác như .h5
        alt_path = OUTPUT_DIR / f"{model_name}_best.h5"
        if alt_path.exists():
            model_path = alt_path
        else:
            return None

    try:
        print(f"[*] Đang nạp mô hình: {model_path}")
        model = tf.keras.models.load_model(str(model_path))
        LOADED_MODELS[model_name] = model
        return model
    except Exception as e:
        print(f"[!] Lỗi khi nạp mô hình {model_name}: {e}")
        return None


def preprocess_image(image_file, model=None, model_name: str = "DenseNet121"):
    """Tiền xử lý ảnh khớp chuẩn động với kích thước và phương thức chuẩn hóa của từng mô hình."""
    # Xác định kích thước ảnh động theo model.input_shape
    target_w, target_h = 224, 224
    if model is not None and hasattr(model, "input_shape") and model.input_shape:
        shape = model.input_shape
        if len(shape) == 4 and shape[1] is not None and shape[2] is not None:
            target_h, target_w = int(shape[1]), int(shape[2])
    elif "densenet" not in model_name.lower():
        target_w, target_h = 128, 128

    img = Image.open(image_file).convert("RGB")
    img = img.resize((target_w, target_h))
    img_array = np.array(img, dtype=np.float32)
    
    name = model_name.lower()
    if "mobilenet" in name:
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    elif "densenet" in name:
        img_array = tf.keras.applications.densenet.preprocess_input(img_array)
    elif "resnet" in name:
        # Nếu model ResNet50 scratch không pretrained thì chuẩn hóa / 255.0
        keras_path = OUTPUT_DIR / f"{model_name}_best.keras"
        if "scratch" in str(keras_path).lower() or not (OUTPUT_DIR / f"{model_name}_pretrained_best.keras").exists():
            img_array = img_array / 255.0
        else:
            img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
    else:
        img_array = img_array / 255.0
        
    img_array = np.expand_dims(img_array, axis=0)  # (1, H, W, 3)
    return img_array


# ==========================================
# CÁC ROUTE GIAO DIỆN & REST API
# ==========================================
@app.route("/")
def index():
    """Trang chủ ứng dụng giao diện VueJS."""
    return render_template("index.html")


@app.route("/api/models", methods=["GET"])
def list_models():
    """Danh sách các mô hình có sẵn trong hệ thống."""
    available = []
    for name in ["MobileNetV2", "ResNet50", "DenseNet121"]:
        keras_file = OUTPUT_DIR / f"{name}_best.keras"
        h5_file = OUTPUT_DIR / f"{name}_best.h5"
        available.append({
            "name": name,
            "trained": keras_file.exists() or h5_file.exists()
        })
    return jsonify({
        "current_model": CURRENT_MODEL_NAME,
        "models": available
    })


@app.route("/api/mushrooms", methods=["GET"])
def get_mushrooms():
    """Tra cứu bách khoa toàn thư 44 loài nấm."""
    species_list = []
    for sc_name, info in MUSHROOM_INFO.items():
        species_list.append(info)
    return jsonify(species_list)


@app.route("/api/mushrooms/<path:scientific_name>", methods=["GET"])
def get_mushroom_detail(scientific_name):
    """Lấy chi tiết một loài nấm."""
    info = MUSHROOM_INFO.get(scientific_name)
    if not info:
        return jsonify({"error": "Không tìm thấy loài nấm này"}), 404
    return jsonify(info)


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Dự đoán loài nấm từ ảnh tải lên.
    Hỗ trợ nhận multipart/form-data từ Web UI hoặc Spring Boot backend.
    """
    if "file" not in request.files:
        return jsonify({"error": "Vui lòng đính kèm file ảnh với trường 'file'"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Chưa chọn file"}), 400

    model_name = request.form.get("model", CURRENT_MODEL_NAME)
    model = get_model(model_name)

    if model is None:
        # Giả lập kết quả mẫu hoặc thông báo mô hình chưa train
        available_files = list(OUTPUT_DIR.glob("*_best.*"))
        if not available_files:
            return jsonify({
                "status": "warning",
                "message": f"Mô hình {model_name} chưa được huấn luyện. Hãy chạy lệnh 'python train.py --model {model_name}' trước!",
                "top_prediction": None,
                "top_5": []
            }), 200

    try:
        # Tiền xử lý khớp kích thước động của mô hình (128x128 hoặc 224x224)
        processed_img = preprocess_image(file, model=model, model_name=model_name)

        # Dự đoán
        preds = model.predict(processed_img)[0]  # Mảng 44 xác suất
        top_indices = np.argsort(preds)[::-1][:5]  # Lấy top 5 index có xác suất cao nhất

        top_5_results = []
        for idx in top_indices:
            sc_name = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"Class_{idx}"
            prob = float(preds[idx])
            info = MUSHROOM_INFO.get(sc_name, {
                "scientific_name": sc_name,
                "vn_name": sc_name,
                "edibility": "unknown",
                "edibility_vn": "Chưa xác định",
                "toxicity_level": "unknown",
                "description": "Chưa có dữ liệu",
                "habitat": "Chưa có dữ liệu"
            })
            top_5_results.append({
                "class_id": int(idx),
                "scientific_name": sc_name,
                "vn_name": info["vn_name"],
                "probability": round(prob * 100, 2),
                "edibility": info["edibility"],
                "edibility_vn": info["edibility_vn"],
                "toxicity_level": info["toxicity_level"],
                "description": info["description"],
                "habitat": info["habitat"]
            })

        return jsonify({
            "status": "success",
            "model_used": model_name,
            "top_prediction": top_5_results[0],
            "top_5": top_5_results
        })

    except Exception as e:
        return jsonify({"error": f"Lỗi trong quá trình xử lý ảnh: {str(e)}"}), 500


if __name__ == "__main__":
    print("[*] Khởi động Flask Server tại http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
