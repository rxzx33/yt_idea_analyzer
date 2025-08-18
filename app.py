import streamlit as st

st.set_page_config(
    page_title="YouTube Shorts Idea Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("YouTube Shorts Idea Analyzer")
st.write("made by Rizal Bintang")

st.markdown("""
Aplikasi sederhana ini membantu kamu menganalisa ide YouTube Shorts kamu dan memberikan feedback berdasarkan potensinya.

## Cara Menggunakan Aplikasi Ini

1. **Persiapkan API Keys**: Dapatkan API Keys dari Google Cloud Console (YouTube Data API) dan Google AI Studio (Gemini API)
2. **Atur Konteks Channel**: Masukkan informasi channel kamu untuk personalisasi analisis
3. **Masukkan API Keys**: Klik "Setup API Keys" di sidebar untuk memasukkan API Keys Anda
4. **Analisis Ide Konten**: Setelah mengatur keduanya, Anda dapat menggunakan fitur analisis ide konten

⚠️ **Catatan Penting**: 
- Kedua langkah pertama (API Keys dan Konteks Channel) harus dilakukan sebelum Anda dapat melakukan analisis
- Untuk hasil terbaik, lengkapi informasi tentang Top 3 Videos kamu di halaman Setup Channel

## Fitur Utama

- **Analisis Potensi Konten**: Menganalisis performa konten berdasarkan data video yang sedang tren
- **Rekomendasi AI Personalisasi**: Memberikan rekomendasi berbasis AI menggunakan Google Gemini yang disesuaikan dengan channel kamu
- **Insight Kompetitor**: Menampilkan informasi tentang kompetitor dan performa video sejenis
- **Personalisasi Channel**: Sesuaikan analisis dengan informasi spesifik tentang channel kamu (menggunakan placeholder data yang aman)

## Privasi Data

- Semua data channel yang dimasukkan hanya disimpan di browser kamu
- Tidak ada data pribadi yang dikirim atau disimpan di server
- Data placeholder default tidak mengandung informasi pribadi apapun

## Kebijakan Penggunaan

- Anda harus menggunakan API Keys Anda sendiri
- Aplikasi ini tidak menyimpan data kamu di server
- Setiap penggunaan API akan dikenakan biaya sesuai ketentuan Google
""")