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
2. **Masuk ke Halaman Setup**: Klik "Setup API Keys" di sidebar untuk memasukkan API Keys Anda
3. **Analisis Ide Konten**: Setelah memasukkan API Keys, Anda dapat menggunakan fitur analisis ide konten

## Fitur Utama

- **Analisis Potensi Konten**: Menganalisis performa konten berdasarkan data video yang sedang tren
- **Rekomendasi AI**: Memberikan rekomendasi berbasis AI menggunakan Google Gemini
- **Insight Kompetitor**: Menampilkan informasi tentang kompetitor dan performa video sejenis

## Kebijakan Penggunaan

- Anda harus menggunakan API Keys Anda sendiri
- Aplikasi ini tidak menyimpan API Keys Anda
- Setiap penggunaan API akan dikenakan biaya sesuai ketentuan Google
""")