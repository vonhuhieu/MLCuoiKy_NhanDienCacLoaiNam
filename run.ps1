# ====================================================================
#   HE THONG NHAN DIEN 44 LOAI NAM (MUSHROOM-44 AI) - 1-CLICK LAUNCHER
# ====================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Mushroom-44 AI System"

Write-Host "====================================================================" -ForegroundColor Green
Write-Host "       HE THONG NHAN DIEN 44 LOAI NAM (MUSHROOM-44 AI)" -ForegroundColor Green
Write-Host "====================================================================" -ForegroundColor Green
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 1. Kiem tra moi truong ao .venv
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "[*] Chua tim thay .venv. Dang tu dong tim kiem Python de khoi tao..." -ForegroundColor Yellow

    $UvPath = Join-Path $env:USERPROFILE ".local\bin\uv.exe"
    if (Test-Path $UvPath) {
        Write-Host "[+] Su dung uv cuc nhanh: $UvPath" -ForegroundColor Cyan
        & $UvPath venv .venv --python 3.11
        & $UvPath pip install --python .venv -r requirements.txt
    } else {
        # Tim Python thong qua Get-Command hoac duong dan pho bien
        $pythonCmd = $null
        try {
            $cmd = Get-Command "py" -ErrorAction SilentlyContinue
            if ($cmd) { $pythonCmd = "py -3" }
        } catch {}

        if (-not $pythonCmd) {
            try {
                $cmd = Get-Command "python" -ErrorAction SilentlyContinue
                if ($cmd) {
                    $ver = & python --version 2>&1
                    if ($ver -match "Python") { $pythonCmd = "python" }
                }
            } catch {}
        }

        if (-not $pythonCmd) {
            $searchPaths = @(
                "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
                "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
                "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
                "C:\Python311\python.exe",
                "C:\Python310\python.exe",
                "C:\Program Files\Python311\python.exe"
            )
            foreach ($p in $searchPaths) {
                if (Test-Path $p) {
                    $pythonCmd = $p
                    break
                }
            }
        }

        if (-not $pythonCmd) {
            Write-Host "[!] KHONG TIM THAY PYTHON TREN MAY CUA BAN!" -ForegroundColor Red
            Write-Host "    Vui long cai dat Python tai https://www.python.org/downloads/ (nho tick Add to PATH)"
            Read-Host "Nhan Enter de thoat..."
            exit 1
        }

        Write-Host "[+] Su dung Python: $pythonCmd" -ForegroundColor Cyan
        Write-Host "[*] Dang tao .venv..." -ForegroundColor Yellow
        Invoke-Expression "$pythonCmd -m venv .venv"

        Write-Host "[*] Dang cai dat dependencies (chi chay 1 lan duy nhat)..." -ForegroundColor Yellow
        & $VenvPython -m pip install --upgrade pip
        & (Join-Path $ScriptDir ".venv\Scripts\pip.exe") install -r requirements.txt
    }
    Write-Host "[+] Khoi tao moi truong ao thanh cong!" -ForegroundColor Green
} else {
    Write-Host "[+] Moi truong ao .venv da san sang." -ForegroundColor Green
}

# 2. Kiem tra model
$ModelPath = Join-Path $ScriptDir "output\DenseNet121_best.keras"
if (Test-Path $ModelPath) {
    Write-Host "[+] Model DenseNet121 da san sang (KHONG CAN TRAIN LAI)." -ForegroundColor Green
} else {
    Write-Host "[!] Chu y: Chua tim thay file model output\DenseNet121_best.keras." -ForegroundColor Yellow
}

# 3. Mo trinh duyet tu dong
Write-Host "[*] Tu dong mo trinh duyet sau 3 giay: http://localhost:5000 ..." -ForegroundColor Cyan
Start-Process "powershell" -ArgumentList "-NoProfile -Command `"Start-Sleep -Seconds 3; Start-Process 'http://localhost:5000'`"" -WindowStyle Hidden

# 4. Khoi chay Web Server
Write-Host ""
Write-Host "====================================================================" -ForegroundColor Green
Write-Host "  Web Server dang chay tai: http://localhost:5000" -ForegroundColor Green
Write-Host "  Nhan Ctrl + C de dung server." -ForegroundColor Yellow
Write-Host "====================================================================" -ForegroundColor Green
Write-Host ""

& $VenvPython app.py

