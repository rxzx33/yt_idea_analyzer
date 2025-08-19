import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from google.generativeai import GenerativeModel
import time
import json
from streamlit_cookies_manager import EncryptedCookieManager
from main import (
    search_youtube_videos,
    get_video_details,
    video_analysis,
)

st.set_page_config(
    page_title="YouTube Shorts Idea Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("📺 YouTube Shorts Idea Analyzer")

st.markdown("""
Aplikasi sederhana ini membantu kamu menganalisa ide YouTube Shorts kamu dan memberikan feedback berdasarkan potensinya.
""")

cookies = EncryptedCookieManager(
    prefix = "yt_shorts_analyzer",
    password = st.secrets["COOKIE_ENCRYPTION_PASSWORD"]
)

if not cookies.ready():
    st.stop()

# Initialize session state for API keys if not already present
if 'yt_api_key' not in st.session_state:
    if cookies.get("yt_api_key"):
        st.session_state.yt_api_key = cookies.get("yt_api_key")
    else:
        st.session_state.yt_api_key = ""

if 'gemini_api_key' not in st.session_state:
    if cookies.get("gemini_api_key"):
        st.session_state.gemini_api_key = cookies.get("gemini_api_key")
    else:
        st.session_state.gemini_api_key = ""

if 'channel_context' not in st.session_state and cookies.get("channel_context"):
    # Load channel context from cookies (stored as JSON string)
    channel_context_json = cookies.get("channel_context")
    try:
        st.session_state.channel_context = json.loads(channel_context_json)
    except (json.JSONDecodeError, TypeError):
        st.session_state.channel_context = None

# Get channel context from session state
channel_context = st.session_state.get('channel_context', {})

# Sidebar for API Key Configuration

with st.sidebar:
    st.header("👋 Selamat Datang!")
    st.markdown("""
    Aplikasi ini dirancang untuk membantu kamu menganalisa ide konten YouTube dan memberikan feedback berdasarkan potensinya.
    Dengan aplikasi ini kamu bisa:
    1. Menganalisa apakah ide konten kamu memiliki potensi untuk mendapatkan banyak views.
    2. Melihat seberapa ketat kompetisi dalam topik tertentu.
    3. Mendapatkan ide hook yang tepat untuk video kamu.
    4. Menghemat waktu dengan memproduksi konten yang berpotensi dan ide yang layak dikejar.
    """)
    st.markdown("---")
    st.header("Cara Menggunakan")
    st.markdown("""
    1. Masukan API Youtube dan Gemini
    2. Masukan informasi channel (niche dan bahasa)
    3. Masukan ide konten yang ingin kamu analisa
    ---
    """)
    
    # API Key input form in sidebar
    st.header("🔑 Input API Keys")
    with st.form("sidebar_api_keys_form"):
        yt_api_key_input = st.text_input(
            "YouTube API Key", 
            value=st.session_state.yt_api_key,
            type="password",
            help="Dapatkan dari Google Cloud Console"
        )
        
        gemini_api_key_input = st.text_input(
            "Gemini API Key", 
            value=st.session_state.gemini_api_key,
            type="password",
            help="Dapatkan dari Google AI Studio"
        )
        
        api_submit = st.form_submit_button("💾 Simpan API Keys")
        
        if api_submit:
            if yt_api_key_input and gemini_api_key_input:
                yt_key_valid = False
                gemini_key_valid = False
                
                # Validate YouTube API Key
                try:
                    youtube_service = build(
                        'youtube',
                        'v3',
                        developerKey=yt_api_key_input
                    )
                    youtube_service.search().list(
                        q='test',
                        part='id',
                        maxResults=1
                    ).execute()
                    yt_key_valid = True
                except Exception as e:
                    st.error(f"❗ YouTube API Error: {str(e)[:50]}...")
                
                # Validate Gemini API Key
                try:
                    genai.configure(api_key=gemini_api_key_input)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    model.generate_content("test")
                    gemini_key_valid = True
                except Exception as e:
                    st.error(f"❗ Gemini API Error: {str(e)[:50]}...")

                if yt_key_valid and gemini_key_valid:
                    st.session_state.yt_api_key = yt_api_key_input
                    st.session_state.gemini_api_key = gemini_api_key_input
                    cookies["yt_api_key"] = yt_api_key_input
                    cookies["gemini_api_key"] = gemini_api_key_input
                    cookies.save()
                    st.success("✅ API Keys tersimpan!")
                    st.rerun()
                else:
                    st.error("❗ Gagal validasi API Keys.")
            else:
                st.error("❗ Masukkan kedua API Keys.")
    
    # Instructions for getting API keys (outside expander)
    with st.expander("📖 **Cara Mendapatkan API Keys:**"):
        st.markdown("""
        **YouTube Data API:**
        1. Buka [Google Cloud Console](https://console.cloud.google.com/)
        2. Buat/pilih project
        3. Aktifkan YouTube Data API v3
        4. Buat API Key di Credentials
        
        Tutorial lengkap bisa diakses [disini](https://developers.google.com/youtube/v3/getting-started?hl=id#before-you-start)
        
        **Gemini API:**
        1. Buka [Google AI Studio](https://aistudio.google.com/)
        2. Login dengan akun Google
        3. Klik "Get API Key"
        """)
    
    st.markdown("---")
    
    # Required Channel Context Setup
    st.header("Informasi Channel")
    with st.form("sidebar_channel_form"):
        niche_input = st.text_input(
            "Niche Channel", 
            value=channel_context.get("niche", ""),
            placeholder="Contoh: Gaming, Edukasi, Hiburan, Teknologi"
        )
        
        language_input = st.selectbox(
            "Bahasa Channel",
            options=["", "Bahasa Indonesia", "English"],
            index=0 if not channel_context.get("language") else 
                    ["", "Bahasa Indonesia", "English"].index(channel_context.get("language", ""))
        )
        
        channel_submit = st.form_submit_button("💾 Simpan Info Channel")
        
        if channel_submit:
            if niche_input and language_input:
                # Update channel context
                updated_context = {
                    "niche": niche_input,
                    "language": language_input
                }
                
                st.session_state.channel_context = updated_context
                cookies["channel_context"] = json.dumps(updated_context)
                cookies.save()
                st.success("✅ Info channel tersimpan!")
                st.rerun()
            else:
                st.error("❗ Mohon isi kedua field untuk menyimpan.")
    
        # Show current channel status
        if st.session_state.get('channel_context') and channel_context.get("niche") and channel_context.get("language"):
            current_niche = channel_context.get("niche")
            current_language = channel_context.get("language")
            st.info(f"📊 Niche: {current_niche} | 🌐 Bahasa: {current_language}")
        elif st.session_state.get('channel_context'):
            st.warning("⚠️ Info channel belum lengkap")
        else:
            st.info("ℹ️ Belum ada info channel")

# Check if API keys are available before proceeding
api_keys_available = st.session_state.get('yt_api_key') and st.session_state.get('gemini_api_key')
if not api_keys_available:
    st.warning("🔐 Silakan masukkan API Keys di sidebar untuk melanjutkan.")
    st.stop()

# Check if channel context is available before proceeding
channel_context_available = (channel_context and 
                            channel_context.get("niche") and 
                            channel_context.get("language"))

if not channel_context_available:
    st.warning("📺 Silakan lengkapi informasi channel (Niche & Bahasa) di sidebar untuk melanjutkan.")
    st.info("Informasi ini diperlukan untuk memberikan analisis yang akurat dan relevan dengan channel kamu.")
    st.stop()

# Get API keys from session state
yt_api_key = st.session_state.yt_api_key
gemini_api_key = st.session_state.gemini_api_key

# Content analysis form
with st.form("content_analysis_form"):
    topic = st.text_input("Masukkan topik atau ide YouTube Shorts kamu", 
                         placeholder="Contoh: Misteri Dunia, Resep Masakan Sehat, Fakta Sejarah")
    
    # Add checkbox for Shorts filter
    shorts_filter = st.checkbox("Gunakan filter #shorts dalam pencarian?", value=True)
    
    submitted = st.form_submit_button("🔍 Analisa Ide Konten")
    
    if submitted:
        if not topic:
            st.error("❗ Mohon masukkan topik atau ide YouTube Shorts kamu.")
        else:
            with st.spinner("🚀 Menganalisis ide konten..."):
                try:
                    # Create YouTube service
                    youtube_service = build(
                        'youtube',
                        'v3',
                        developerKey=yt_api_key
                    )
                    
                    # Create Gemini model
                    genai.configure(api_key=gemini_api_key)
                    generation_config = {
                        'temperature': 0.2,
                        'top_p': 0.8,
                        'top_k': 1,
                    }
                    gemini_model = GenerativeModel(
                        model_name='gemini-2.5-flash',
                        generation_config=generation_config
                    )
                    
                    # Modify search query based on filter
                    search_query = topic
                    if shorts_filter:
                        search_query += " #shorts"
                    
                    # Search for videos
                    search_results = search_youtube_videos(youtube_service, search_query, max_results=20)
                    
                    if search_results:
                        st.write(f"📊 Menemukan {len(search_results)} video potensial (mengambil detail...)")
                        
                        # Get video IDs
                        video_ids_to_fetch = [video['videoId'] for video in search_results if video.get('videoId')]
                        
                        # Get video details
                        video_details = get_video_details(youtube_service, video_ids_to_fetch)
                        
                        if video_details:
                            # Perform analysis
                            analysis_output = video_analysis(search_results, video_details)
                            
                            if analysis_output:
                                # Prepare LLM prompt
                                llm_prompt = f"""
                                Anda adalah seorang ahli strategi pemasaran digital YouTube Shorts yang berpengalaman dan tajam.
                                Tugas Anda adalah menganalisis potensi ide konten yang disajikan dan memberikan rekomendasi yang jelas, singkat, dan langsung pada intinya.

                                Berikut adalah data analisis video Shorts terkait ide konten yang dicari. Data ini kini sangat kaya, mencakup detail per video seperti judul, ID, jumlah penayangan, tanggal publikasi, durasi, jumlah suka (likeCount), jumlah komentar (commentCount), dan tingkat keterlibatan (engagementRate). Ringkasan keseluruhan juga menyertakan rata-rata tingkat keterlibatan (averageEngagementRate). **Harap perhatikan juga 'currentTimestamp' yang menunjukkan waktu analisis dilakukan, untuk membantu Anda menilai usia video.**
                                {json.dumps(analysis_output, indent=2)}

                                ---
                                
                                Konteks channel YouTube saya untuk analisis ini:
                                - Niche Channel: {channel_context.get("niche")}
                                - Bahasa Channel: {channel_context.get("language")}
                                
                                Mohon berikan analisis yang disesuaikan dengan niche dan bahasa channel saya.
                                
                                ---

                                Berdasarkan data video yang relevan di atas, dan dengan mempertimbangkan konteks saluran saya, berikan analisis komprehensif tentang potensi ide konten ini di YouTube Shorts.
                                
                                Fokus utama analisis Anda adalah membantu saya memutuskan: **Apakah ide konten ini layak dikejar untuk saluran YouTube Shorts saya?**
                                
                                **RESPONSE FORMAT:**
                                Sampaikan analisis Anda dalam format berikut, dengan jawaban yang sangat ringkas dan langsung pada inti.

                                **💡 Rekomendasi Hasil Analisis:**
                                [Sertakan keputusan yang jelas: "SANGAT LAYAK DIKEJAR", "LAYAK DIKEJAR", "KURANG LAYAK DIKEJAR", atau "TIDAK LAYAK DIKEJAR". Pilih salah satu dari empat opsi ini. Pastikan untuk memberikan keputusan yang tegas berdasarkan analisis Anda.]

                                **❓ Mengapa?:**
                                [Jelaskan alasan utama untuk keputusan di atas secara ringkas. Fokus pada DEMAND, KOMPETISI, dan RELEVANSI dengan channel Anda. Beri penilaian yang jujur dan realistis. Contoh: "Permintaan tinggi, kompetisi moderat, sangat cocok dengan niche Anda." atau "Permintaan ada tapi kompetisi terlalu tinggi untuk channel kecil." atau "Topik tidak relevan dengan audiens Anda."]

                                **🚀 Potensi Konten:**
                                [Jelaskan secara singkat apakah ada minat yang jelas dari audiens untuk topik ini, berdasarkan metrik penayangan dan keterlibatan. Gunakan bahasa naratif, hindari nama kunci JSON. Contoh: "Penayangan rata-rata sangat tinggi dengan beberapa video viral yang mencapai jutaan views, menunjukkan minat pasar yang masif. Tingkat keterlibatan juga cukup sehat."]

                                **🎯 Ide Hooks:**
                                [Berikan 2-3 ide 'hook' yang menarik dan singkat (untuk 3 detik pertama) untuk video Shorts ini, yang relevan dengan topik dan mampu menarik perhatian penonton secara instan.]

                                **Saran Hashtag & Deskripsi Singkat:**
                                [Berikan 2-3 hashtag yang paling relevan untuk meningkatkan visibilitas video. Sertakan juga contoh deskripsi singkat (1-2 kalimat) yang dapat digunakan, dengan kata kunci relevan.]
                                
                                **✨ Strategi:**
                                [Sertakan 1-2 saran tentang taktik atau sudut pandang konten yang unik berdasarkan analisis persaingan, agar video Anda bisa menonjol di niche ini. Ini bisa berupa gaya penyampaian, elemen visual, atau format cerita.]

                                **➡️ Saran Call to Action (CTA):**
                                [Berikan 1-2 ide 'Call to Action' (CTA) yang efektif dan relevan untuk video Shorts ini, mendorong interaksi penonton seperti like, komentar, subscribe, atau kunjungan link di deskripsi.]

                                RESPONSE RULES:
                                1. **MULAI LANGSUNG DENGAN ANALISIS:** Jangan berikan pengenalan atau salam. Langsung mulai dengan analisis poin pertama ("1. Potensi Pasar & Audiens").
                                2. **Format jawaban Anda dengan jelas, menggunakan daftar poin dan paragraf yang mudah dibaca, serta berikan rekomendasi yang spesifik dan dapat ditindaklanjuti.**
                                3. **Mohon sampaikan analisis Anda dalam bahasa yang alami dan mudah dipahami oleh pembuat konten, tanpa mengacu langsung pada nama-nama kunci data JSON seperti viewCount, videoAgeDays, highestViews, dll. Terjemahkan data tersebut menjadi narasi yang ringkas dan relevan.**
                                4. **Jika kamu perlu menyebutkan video tertentu, gunakan judul video tersebut sebagai referensi, bukan ID video.**
                                5. **Berikan penilaian yang tajam, jujur, dan realistis.**
                                6. **PENTING: Jangan ragu menyatakan jika ide konten ini tidak layak dikejar.**
                                7. **HANYA BERIKAN JAWABAN SESUAI FORMAT DI ATAS.** Pastikan setiap bagian dalam format respons terisi.
                                8. **PENTING (Kondisional): Jika [Keputusan Akhir] adalah "KURANG LAYAK DIKEJAR" atau "TIDAK LAYAK DIKEJAR", maka JANGAN SERTAKAN bagian '[Saran Judul & Ide Konten Tambahan]', '[🎯 Saran Hooks (3 Detik Pertama)]', '[✨ Taktik & Sudut Pandang Unik]', '[➡️ Saran Call to Action (CTA)]', dan '[# Saran Hashtag & Deskripsi Singkat]'. Akhiri respons setelah bagian '[Mengapa?]'.**
                                """

                                gemini_response = None
                                api_error = None
                                
                                try:
                                    gemini_response = gemini_model.generate_content(llm_prompt)
                                except Exception as e:
                                    api_error = e

                                if api_error:
                                    st.error(f"Terjadi kesalahan saat mengakses API: {str(api_error)}")
                                elif gemini_response:
                                    gemini_analysis_text = gemini_response.text
                                    st.success("Analisa selesai!")
                                    st.subheader("Hasil Analisa Konten")
                                    st.markdown(gemini_analysis_text)
                                else:
                                    st.warning("Tidak ada data yang tersedia untuk analisis.")

                                # Display summary metrics
                                st.subheader("📈 Ringkasan Analisis")
                                col1, col2, col3, col4 = st.columns(4)
                                col1.metric("Total Video", analysis_output.get('totalVideos', 'N/A'))
                                col2.metric("Total Penayangan", f"{analysis_output.get('totalViews', 0):,}")
                                col3.metric("Rata-rata Penayangan", f"{analysis_output.get('averageViews', 0):,}")
                                col4.metric("Rata-rata Engagement Rate", analysis_output.get('averageEngagementRate', 'N/A'))
                                
                                # Display top performers
                                top_videos = analysis_output.get('topPerformers', [])
                                
                                if top_videos:
                                    st.subheader(f"5 Video Teratas untuk pencarian '{search_query}'")
                                    for i, video in enumerate(top_videos, start=1):
                                        views_formatted = f"{video.get('viewCount', 'N/A'):,}" if isinstance(video.get('viewCount'), (int, float)) else video.get('viewCount', 'N/A')
                                        st.write(f"**{i}. {video.get('title', 'N/A')}**")
                                        st.write(f"👁️ Penayangan: {views_formatted} | 👍 Suka: {video.get('likeCount', 'N/A')} | 📊 Engagement Rate: {video.get('engagementRate', 'N/A')}")
                                        st.markdown("---")
                                    
                                    st.info("""
                                    ℹ️ **Catatan:**
                                    - Engagement Rate dihitung sebagai (Jumlah Suka + Jumlah Komentar) / Jumlah Penayangan
                                    - Video dengan engagement rate yang lebih tinggi menunjukkan potensi yang lebih baik untuk ide konten Anda
                                    """)
                            else:
                                st.error("❌ Tidak ada hasil analisis yang dihasilkan.")
                        else:
                            st.error("❌ Gagal mengambil detail video. Mohon periksa kembali API Key YouTube Anda.")
                    else:
                        st.error("❌ Tidak ada hasil pencarian video. Mohon coba dengan kata kunci lain.")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {str(e)}")
                    st.write("Mohon pastikan API keys Anda benar dan Anda memiliki kuota yang cukup.")
