#!/usr/bin/env bash
# ====================================================================
#   HE THONG NHAN DIEN 44 LOAI NAM (MUSHROOM-44 AI) - 1-CLICK LAUNCHER
# ====================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "===================================================================="
echo "       HE THONG NHAN DIEN 44 LOAI NAM (MUSHROOM-44 AI)"
echo "===================================================================="
echo ""

# 1. Kiem tra moi truong ao .venv
if [ ! -f ".venv/bin/python" ]; then
    echo "[*] Chua tim thay .venv. Dang tu dong tao moi truong ao..."
    if command -v uv &> /dev/null; then
        echo "[+] Su dung uv..."
        uv venv .venv --python 3.11
        uv pip install --python .venv -r requirements.txt
    elif command -v python3 &> /dev/null; then
        python3 -m venv .venv
        .venv/bin/pip install --upgrade pip
        .venv/bin/pip install -r requirements.txt
    elif command -v python &> /dev/null; then
        python -m venv .venv
        .venv/bin/pip install --upgrade pip
        .venv/bin/pip install -r requirements.txt
    else
        echo "[!] Khong tim thay Python. Vui long cai dat Python 3.10 hoac 3.11!"
        exit 1
    fi
    echo "[+] Cai dat moi truong ao hoan tat!"
else
    echo "[+] Moi truong ao .venv da san sang."
fi

# 2. Kiem tra file model
if [ -f "output/DenseNet121_best.keras" ]; then
    echo "[+] Model DenseNet121 da san sang (KHONG CAN TRAIN LAI)."
else
    echo "[!] Canh bao: Chua co file model output/DenseNet121_best.keras"
fi

# 3. Tu dong mo trinh duyet sau 3 giay
(sleep 3 && {
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:5000"
    elif command -v open &> /dev/null; then
        open "http://localhost:5000"
    fi
} &) > /dev/null 2>&1

# 4. Khoi chay Web Server
echo ""
echo "===================================================================="
echo "  Server dang hoat dong tai: http://localhost:5000"
echo "  Nhan Ctrl + C de dung server."
echo "===================================================================="
echo ""

.venv/bin/python app.py

