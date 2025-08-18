@echo off
color 0A

:: --- Pesan Selamat Datang ---
echo ===============================================
echo   SCRIPT PENYIAPAN LINGKUNGAN PROYEK PYTHON
echo ===============================================
echo.
echo Script ini akan membantu Anda menyiapkan proyek:
echo 1. Memastikan Python 3 terinstal.
echo 2. Membuat lingkungan virtual (venv).
echo 3. Menginstal semua pustaka yang dibutuhkan.
echo 4. Meminta dan menyimpan kunci API Anda ke file .env.
echo.

:: --- Cek Python ---
echo Mengecek instalasi Python...
python -c "exit()" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ditemukan atau tidak ada di PATH Anda. Mohon instal Python 3 terlebih dahulu.
    echo Kunjungi: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python ditemukan.

:: --- Buat Lingkungan Virtual (venv) ---
echo Mengecek/membuat lingkungan virtual (venv)...
if not exist "venv" (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Gagal membuat lingkungan virtual. Pastikan Python 3 terinstal dengan benar.
        pause
        exit /b 1
    )
    echo Lingkungan virtual 'venv' berhasil dibuat.
) else (
    echo Lingkungan virtual 'venv' sudah ada.
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

:: --- Instal Dependensi ---
echo Menginstal pustaka yang dibutuhkan dari requirements.txt...
if not exist "requirements.txt" (
    echo ERROR: File 'requirements.txt' tidak ditemukan di direktori ini.
    echo Mohon pastikan file tersebut ada.
    pause
    exit /b 1
)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Gagal menginstal pustaka. Mohon periksa koneksi internet Anda atau coba secara manual:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)
echo Semua pustaka berhasil diinstal.

:: --- Minta dan Simpan Kunci API ke .env ---
echo.
echo ===============================================
echo        PENGATURAN KUNCI API (API KEYS)
echo ===============================================
echo Anda memerlukan kunci API YouTube Data API v3 dan Google Gemini API.
echo Lihat README.md untuk instruksi cara mendapatkannya.
echo.

set /p YOUTUBE_API_KEY="Masukkan Kunci API YouTube Anda (YOUTUBE_API_KEY): "
set /p GEMINI_API_KEY="Masukkan Kunci API Google Gemini Anda (GEMINI_API_KEY): "

echo Menyimpan kunci API ke file .env...
:: Cek apakah .env sudah ada, jika ada, tanyakan untuk menimpa
if exist ".env" (
    set /p overwrite_choice="File .env sudah ada. Timpa dengan kunci baru (y/N)? "
    if /i "%overwrite_choice%"=="y" (
        echo YOUTUBE_API_KEY=%YOUTUBE_API_KEY%> .env
        echo GEMINI_API_KEY=%GEMINI_API_KEY%>> .env
        echo File .env berhasil ditimpa dengan kunci baru.
    ) else (
        echo File .env TIDAK ditimpa. Mohon edit file .env secara manual untuk memperbarui kunci.
    )
) else (
    echo YOUTUBE_API_KEY=%YOUTUBE_API_KEY%> .env
    echo GEMINI_API_KEY=%GEMINI_API_KEY%>> .env
    echo File .env berhasil dibuat dengan kunci API Anda.
)

:: --- Instruksi Selanjutnya ---
echo.
echo ===============================================
echo           PENYIAPAN SELESAI!
echo ===============================================
echo.
echo Lingkungan virtual Anda sudah diatur dan kunci API telah disimpan.
echo Anda sekarang dapat menjalankan script utama:
echo.
echo   python main.py
echo.
echo Penting: Lingkungan virtual sudah aktif di command prompt ini. Jika Anda menutup jendela dan membukanya lagi, Anda perlu mengaktifkannya kembali dengan:
echo   venv\Scripts\activate.bat
echo.
pause