import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
from google.generativeai import GenerativeModel
from datetime import datetime
import json
import textwrap
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

if 'yt_api_key' not in st.session_state and cookies.get("yt_api_key"):
    st.session_state.yt_api_key = cookies.get("yt_api_key")

if 'gemini_api_key' not in st.session_state and cookies.get("gemini_api_key"):
    st.session_state.gemini_api_key = cookies.get("gemini_api_key")

if 'channel_context' not in st.session_state and cookies.get("channel_context"):
    st.session_state.channel_context = cookies.get("channel_context")

# Import functions from main.py
from main import (
    search_youtube_videos,
    get_video_details,
    video_analysis,
    safe_int_convert
)

st.set_page_config(
    page_title="Analisis Ide Konten - YouTube Shorts Idea Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analisis Ide Konten YouTube Shorts")

# Check if API keys and channel context are available
api_keys_available = st.session_state.get('yt_api_key') and st.session_state.get('gemini_api_key')
channel_context_available = st.session_state.get('channel_context') is not None

if not api_keys_available and not channel_context_available:
    st.warning("🔐 Baik API Keys maupun Informasi Channel belum diatur.")
    st.info("Silakan masuk ke halaman 'Setup API Keys' dan 'Setup Channel Context' terlebih dahulu.")
    st.stop()
elif not api_keys_available:
    st.warning("🔑 API Keys belum diatur. Silakan masuk ke halaman 'Setup API Keys' terlebih dahulu.")
    st.stop()
elif not channel_context_available:
    st.warning("📺 Informasi Channel belum diatur. Silakan masuk ke halaman 'Setup Channel Context' terlebih dahulu.")
    st.stop()

# Get channel context from session state
channel_context = st.session_state.get('channel_context', {})

# Second gatekepper to ensure accuracy in AI analysis by checking top videos
top_videos = channel_context.get('top_videos', [])

if not top_videos:
    st.warning("Top videos tidak ditemukan. Mohon periksa kembali informasi channel dan coba lagi.")
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
            with st.spinner("🔍 Analisis sedang dilakukan..."):
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
                    
                    st.write(f"🔍 Mencari video dengan keyword: {search_query}")
                    
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
                                st.success("✅ Analisis berhasil dilakukan!")
                                
                                # Display summary metrics
                                st.subheader("📈 Ringkasan Analisis")
                                col1, col2, col3, col4 = st.columns(4)
                                col1.metric("Total Video", analysis_output.get('totalVideos', 'N/A'))
                                col2.metric("Total Penayangan", f"{analysis_output.get('totalViews', 0):,}")
                                col3.metric("Rata-rata Penayangan", f"{analysis_output.get('averageViews', 0):,}")
                                col4.metric("Engagement Rate", analysis_output.get('averageEngagementRate', 'N/A'))
                                
                                # Display top performers
                                top_videos = analysis_output.get('topPerformers', [])
                                
                                if top_videos:
                                    st.subheader(f"🏆 5 Video Teratas untuk pencarian '{search_query}'")
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
                                
                                # Use channel context data from session state (already validated above)
                                # We don't need a fallback here since we've already checked for its existence
                                
                                # Prepare LLM prompt
                                llm_prompt = f"""
                                Anda adalah seorang ahli strategi pemasaran digital YouTube Shorts yang berpengalaman dan tajam.
                                Tugas Anda adalah menganalisis potensi ide konten yang disajikan dan memberikan rekomendasi yang jelas, singkat, dan langsung pada intinya.

                                Berikut adalah data analisis video Shorts terkait ide konten yang dicari. Data ini kini sangat kaya, mencakup detail per video seperti judul, ID, jumlah penayangan, tanggal publikasi, durasi, jumlah suka (likeCount), jumlah komentar (commentCount), dan tingkat keterlibatan (engagementRate). Ringkasan keseluruhan juga menyertakan rata-rata tingkat keterlibatan (averageEngagementRate). **Harap perhatikan juga 'currentTimestamp' yang menunjukkan waktu analisis dilakukan, untuk membantu Anda menilai usia video.**
                                {json.dumps(analysis_output, indent=2)}

                                ---
                                
                                Konteks channel YouTube saya untuk kebutuhan untuk analisis ini:
                                {json.dumps(channel_context, indent=2)}
                                
                                ---

                                Berdasarkan data video yang relevan di atas, dan dengan mempertimbangkan konteks saluran saya, berikan analisis komprehensif tentang potensi ide konten ini di YouTube Shorts.
                                
                                Fokus utama analisis Anda adalah membantu saya memutuskan: **Apakah ide konten ini layak dikejar untuk saluran YouTube Shorts saya?**
                                
                                **RESPONSE FORMAT:**
                                Sampaikan analisis Anda dalam format berikut, dengan jawaban yang sangat ringkas dan langsung pada inti.

                                [💡 Rekomendasi Hasil Analisis]:
                                [Sertakan keputusan yang jelas: "SANGAT LAYAK DIKEJAR", "LAYAK DIKEJAR", "KURANG LAYAK DIKEJAR", atau "TIDAK LAYAK DIKEJAR". Pilih salah satu dari empat opsi ini. Pastikan untuk memberikan keputusan yang tegas berdasarkan analisis Anda.]

                                [❓ Mengapa?]:
                                [Jelaskan alasan utama untuk keputusan di atas secara ringkas. Fokus pada DEMAND, KOMPETISI, dan RELEVANSI dengan channel Anda. Beri penilaian yang jujur dan realistis. Contoh: "Permintaan tinggi, kompetisi moderat, sangat cocok dengan niche Anda." atau "Permintaan ada tapi kompetisi terlalu tinggi untuk channel kecil." atau "Topik tidak relevan dengan audiens Anda."]

                                [🚀 Potensi Konten]:
                                [Jelaskan secara singkat apakah ada minat yang jelas dari audiens untuk topik ini, berdasarkan metrik penayangan dan keterlibatan. Gunakan bahasa naratif, hindari nama kunci JSON. Contoh: "Penayangan rata-rata sangat tinggi dengan beberapa video viral yang mencapai jutaan views, menunjukkan minat pasar yang masif. Tingkat keterlibatan juga cukup sehat."]

                                **[🎯 Ide Hooks]:**
                                [Berikan 2-3 ide 'hook' yang menarik dan singkat (untuk 3 detik pertama) untuk video Shorts ini, yang relevan dengan topik dan mampu menarik perhatian penonton secara instan.]

                                **[# Saran Hashtag & Deskripsi Singkat]:**
                                [Berikan 2-3 hashtag yang paling relevan untuk meningkatkan visibilitas video. Sertakan juga contoh deskripsi singkat (1-2 kalimat) yang dapat digunakan, dengan kata kunci relevan.]
                                
                                **[✨ Strategi]:**
                                [Sertakan 1-2 saran tentang taktik atau sudut pandang konten yang unik berdasarkan analisis persaingan, agar video Anda bisa menonjol di niche ini. Ini bisa berupa gaya penyampaian, elemen visual, atau format cerita.]

                                **[➡️ Saran Call to Action (CTA)]:**
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
                                
                                st.write("🧠 Menghasilkan rekomendasi AI...")
                                
                                # Generate content with Gemini
                                gemini_response = gemini_model.generate_content(llm_prompt)
                                gemini_analysis_text = gemini_response.text
                                
                                st.subheader("🤖 Hasil Analisa Konten oleh AI")
                                st.markdown(gemini_analysis_text)
                            else:
                                st.error("❌ Tidak ada hasil analisis yang dihasilkan.")
                        else:
                            st.error("❌ Gagal mengambil detail video. Mohon periksa kembali API Key YouTube Anda.")
                    else:
                        st.error("❌ Tidak ada hasil pencarian video. Mohon coba dengan kata kunci lain.")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {str(e)}")
                    st.write("Mohon pastikan API keys Anda benar dan Anda memiliki kuota yang cukup.")