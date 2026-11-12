@echo off
chcp 65001 >nul
title He Thong Nhan Dien Cac Loai Nam - Mushroom-44 AI
echo ====================================================================
echo        HE THONG NHAN DIEN 44 LOAI NAM (MUSHROOM-44 AI)
echo ====================================================================
echo.

cd /d "%~dp0"

REM 1. Kiem tra xem moi truong ao .venv da san sang chua
if exist ".venv\Scripts\python.exe" (
    echo [+] Da tim thay moi truong ao .venv co san.
    goto check_model
)

echo [*] Phat hien chua co moi truong ao. Dang tu dong tim kiem Python tren may...

set "PY_CMD="

REM Kiem tra uv truoc (neu co thi rat nhanh)
if exist "%USERPROFILE%\.local\bin\uv.exe" (
    echo [+] Phat hien uv tai: %USERPROFILE%\.local\bin\uv.exe
    echo [*] Dang tao .venv bang uv...
    "%USERPROFILE%\.local\bin\uv.exe" venv .venv --python 3.11
    if exist ".venv\Scripts\python.exe" (
        echo [*] Dang cai dat dependencies bang uv...
        "%USERPROFILE%\.local\bin\uv.exe" pip install --python .venv -r requirements.txt
        goto check_model
    )
)

REM Kiem tra py launcher cua Windows
py -3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=py -3"
    goto create_venv
)

REM Kiem tra python tieu chuan
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python"
    goto create_venv
)

REM Kiem tra python3
python3 --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PY_CMD=python3"
    goto create_venv
)

REM Quet thu muc cai dat Python pho bien tren Windows
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
) do (
    if exist "%%~p" (
        set "PY_CMD=%%~p"
        goto create_venv
    )
)

echo [!] KHONG TIM THAY PYTHON TREN MAY CUA BAN!
echo     Vui long tai va cai dat Python tu: https://www.python.org/downloads/
echo     Luu y: Tich chon Add python.exe to PATH khi cai dat.
echo.
pause
exit /b 1

:create_venv
echo [+] Su dung trinh thong dich: %PY_CMD%
echo [*] Dang khoi tao moi truong ao .venv...
%PY_CMD% -m venv .venv
if %ERRORLEVEL% neq 0 (
    echo [!] Khoi tao .venv that bai!
    pause
    exit /b 1
)

echo [*] Dang cai dat cac thu vien can thiet tu requirements.txt...
echo     Qua trinh nay chi chay 1 lan duy nhat khi moi clone ve.
call .venv\Scripts\python.exe -m pip install --upgrade pip
call .venv\Scripts\pip.exe install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [!] Cai dat dependencies that bai! Vui long kiem tra ket noi mang.
    pause
    exit /b 1
)
echo [+] Cai dat moi truong hoan tat!

:check_model
if not exist "output\DenseNet121_best.keras" (
    echo [!] Canh bao: Khong tim thay file model output\DenseNet121_best.keras
) else (
    echo [+] Model DenseNet121 san sang - KHONG CAN TRAIN LAI.
)

REM 2. Tu dong mo trinh duyet sau 3 giay
echo [*] Dang khoi dong Web Server tai http://localhost:5000 ...
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://localhost:5000"

REM 3. Chay Flask Server
echo.
echo ====================================================================
echo   Server dang hoat dong tai http://localhost:5000
echo   Nhan Ctrl+C de dung server khi muon thoat.
echo ====================================================================
echo.
call .venv\Scripts\python.exe app.py

pause
