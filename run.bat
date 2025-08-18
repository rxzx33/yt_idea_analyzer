@echo off
color 0B

:: --- Pesan Selamat Datang ---
echo ===============================================
echo         MENJALANKAN PROYEK PYTHON
echo ===============================================
echo.

:: --- Cek Lingkungan Virtual ---
if not exist "venv" (
    echo ERROR: Lingkungan virtual 'venv' tidak ditemukan.
    echo Mohon jalankan script penyiapan (setup.bat) terlebih dahulu.
    pause
    exit /b 1
)

:: --- Aktifkan Lingkungan Virtual ---
echo Mengaktifkan lingkungan virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Gagal mengaktifkan lingkungan virtual. Mohon coba secara manual:
    echo   venv\Scripts\activate.bat
    pause
    exit /b 1
)
echo Lingkungan virtual 'venv' berhasil diaktifkan.

:: --- Jalankan Script Utama ---
echo Menjalankan script utama (main.py)...
python main.py
if %errorlevel% neq 0 (
    echo ERROR: Script utama (main.py) gagal dijalankan.
    echo Mohon periksa error di atas.
    call venv\Scripts\deactivate.bat
    pause
    exit /b 1
)

echo.
echo ===============================================
echo           EKSEKUSI SELESAI
echo ===============================================
echo.
call venv\Scripts\deactivate.bat :: Nonaktifkan lingkungan virtual setelah selesai (opsional)
pause :: Jeda agar jendela tidak langsung tertutup