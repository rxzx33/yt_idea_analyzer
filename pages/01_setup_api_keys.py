import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix = "yt_shorts_analyzer",
    password = st.secrets["COOKIE_ENCRYPTION_PASSWORD"]
)

st.set_page_config(
    page_title="YouTube Shorts Idea Analyzer",
    page_icon="📺",
    layout="wide"
)

if not cookies.ready():
    st.stop()

st.set_page_config(
    page_title="Setup API Keys - YouTube Shorts Idea Analyzer",
    page_icon="🔑",
    layout="centered"
)

st.title("🔑 Setup API Keys")

st.markdown("""
Untuk menggunakan aplikasi ini, kamu perlu memasukkan API Keys dari:
1. **YouTube Data API** - untuk menganalisis video YouTube
2. **Google Gemini API** - untuk mendapatkan rekomendasi berbasis AI

API Keys kamu akan disimpan secara lokal di browser kamu dan tidak akan dikirim ke server manapun.
""")

# Initialize session state for API keys if not already present
if 'yt_api_key' not in st.session_state and cookies.get("yt_api_key"):
    st.session_state.yt_api_key = cookies.get("yt_api_key")
if 'gemini_api_key' not in st.session_state and cookies.get("gemini_api_key"):
    st.session_state.gemini_api_key = cookies.get("gemini_api_key")

# Create form for API key entry
with st.form("api_keys_form"):
    st.subheader("YouTube Data API Key")
    yt_api_key = st.text_input(
        "Masukkan YouTube API Key", 
        value=st.session_state.yt_api_key,
        type="password",
        help="Dapatkan dari Google Cloud Console"
    )
    
    st.subheader("Google Gemini API Key")
    gemini_api_key = st.text_input(
        "Masukkan Gemini API Key", 
        value=st.session_state.gemini_api_key,
        type="password",
        help="Dapatkan dari Google AI Studio"
    )
    
    st.info("ℹ️ API Keys hanya akan disimpan di session browser kamu dan tidak akan dikirim ke server manapun.")
    
    submitted = st.form_submit_button("Simpan API Keys")
    
    if submitted:
        if yt_api_key and gemini_api_key:
            yt_key_valid = False
            gemini_key_valid = False
            try:
                youtube_service = build(
                    'youtube',
                    'v3',
                    developerKey=yt_api_key
                )
                youtube_service.search().list(
                    q='test',
                    part='id',
                    maxResults=1
                )
                yt_key_valid = True
            except Exception as e:
                st.error(f"❗ Gagal menghubungkan ke YouTube API: {e}")
            try:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                model.generate_content("test")
                gemini_key_valid = True
            except Exception as e:
                st.error(f"❗ Gagal menghubungkan ke Gemini API: {e}")

            if yt_key_valid and gemini_key_valid:
                st.session_state.yt_api_key = yt_api_key
                st.session_state.gemini_api_key = gemini_api_key
                cookies["yt_api_key"] = yt_api_key
                cookies["gemini_api_key"] = gemini_api_key
                cookies.save()
                st.success("✅ API Keys berhasil disimpan!")
                st.info("Sekarang kamu bisa masuk ke halaman 'Analisis Ide Konten' untuk mulai menggunakan aplikasi.")
            else:
                st.error("❗ Gagal menyimpan API Keys. Pastikan kedua API Keys valid.")
        else:
            st.error("❗ Mohon masukkan kedua API Keys untuk melanjutkan.")

# Instructions for getting API keys
st.markdown("---")
st.subheader("Cara Mendapatkan API Keys")

with st.expander("📺 YouTube Data API Key"):
    st.markdown("""
    1. Kunjungi [Google Cloud Console](https://console.cloud.google.com/)
    2. Buat project baru atau pilih project yang sudah ada
    3. Buka "APIs & Services" > "Enabled APIs & Services"
    4. Cari dan aktifkan "YouTube Data API v3"
    5. Buka "APIs & Services" > "Credentials"
    6. Klik "CREATE CREDENTIALS" > "API Key"
    7. Salin dan simpan API Key yang dihasilkan
    """)

with st.expander("🤖 Google Gemini API Key"):
    st.markdown("""
    1. Kunjungi [Google AI Studio](https://aistudio.google.com/)
    2. Masuk dengan akun Google kamu
    3. Klik "Get API Key" atau navigasi ke "Get API key in Google Cloud"
    4. Buat dan salin API Key kamu
    """)