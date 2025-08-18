#!/bin/bash

# --- Pesan Selamat Datang ---
echo "==============================================="
echo "  SCRIPT PENYIAPAN LINGKUNGAN PROYEK PYTHON"
echo "==============================================="
echo ""
echo "Script ini akan membantu Anda menyiapkan proyek:"
echo "1. Memastikan Python 3 terinstal."
echo "2. Membuat lingkungan virtual (venv)."
echo "3. Menginstal semua pustaka yang dibutuhkan."
echo ""

# --- Cek Python 3 ---
echo "Mengecek instalasi Python 3..."
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 tidak ditemukan. Mohon instal Python 3 terlebih dahulu."
    echo "Kunjungi: https://www.python.org/downloads/"
    exit 1
fi
echo "Python 3 ditemukan."

# --- Buat Lingkungan Virtual (venv) ---
echo "Mengecek/membuat lingkungan virtual (venv)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Gagal membuat lingkungan virtual. Pastikan Python 3 terinstal dengan benar."
        exit 1
    fi
    echo "Lingkungan virtual 'venv' berhasil dibuat."
else
    echo "Lingkungan virtual 'venv' sudah ada."
fi

# --- Aktifkan Lingkungan Virtual ---
echo "Mengaktifkan lingkungan virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal mengaktifkan lingkungan virtual. Mohon coba secara manual:"
    echo "  source venv/bin/activate"
    exit 1
fi
echo "Lingkungan virtual 'venv' berhasil diaktifkan."

# --- Instal Dependensi ---
echo "Menginstal pustaka yang dibutuhkan dari requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: File 'requirements.txt' tidak ditemukan di direktori ini."
    echo "Mohon pastikan file tersebut ada."
    exit 1
fi
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Gagal menginstal pustaka. Mohon periksa koneksi internet Anda atau coba secara manual:"
    echo "  pip install -r requirements.txt"
    exit 1
fi
echo "Semua pustaka berhasil diinstal."

# --- Instruksi Selanjutnya ---
echo ""
echo "==============================================="
echo "           PENYIAPAN SELESAI!"
echo "==============================================="
echo ""
echo "Langkah selanjutnya yang perlu Anda lakukan:"
echo "1. Dapatkan kunci API YouTube Data API v3 dan Google Gemini API."
echo "   Lihat README.md untuk instruksi lebih lanjut."
echo "2. Buat file .env di direktori ini, dan masukkan kunci API Anda:"
echo "   YOUTUBE_API_KEY=KUNCI_API_YOUTUBE_ANDA"
echo "   GEMINI_API_KEY=KUNCI_API_GEMINI_ANDA"
echo "3. Setelah kunci API Anda siap, jalankan script utama:"
echo "   python main.py"
echo ""
echo "Penting: Lingkungan virtual sudah aktif di terminal ini. Jika Anda menutup terminal dan membukanya lagi, Anda perlu mengaktifkannya kembali dengan:"
echo "  source venv/bin/activate"
echo ""