#!/bin/bash

# --- Pesan Selamat Datang ---
echo "==============================================="
echo "        MENJALANKAN PROYEK PYTHON"
echo "==============================================="
echo ""

# --- Cek Lingkungan Virtual ---
if [ ! -d "venv" ]; then
    echo "ERROR: Lingkungan virtual 'venv' tidak ditemukan."
    echo "Mohon jalankan script penyiapan (./setup.sh) terlebih dahulu."
    exit 1
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

# --- Jalankan Script Utama ---
echo "Menjalankan script utama (main.py)..."
python main.py
if [ $? -ne 0 ]; then
    echo "ERROR: Script utama (main.py) gagal dijalankan."
    echo "Mohon periksa error di atas."
    deactivate # Nonaktifkan venv jika terjadi error
    exit 1
fi

echo ""
echo "==============================================="
echo "           EKSEKUSI SELESAI"
echo "==============================================="
echo ""
deactivate # Nonaktifkan lingkungan virtual setelah selesai (opsional)