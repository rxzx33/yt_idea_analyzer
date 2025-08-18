# Main functions for YouTube Shorts Analyzer
from googleapiclient.discovery import build
import google.generativeai as genai
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
from datetime import datetime
import json
import os
import textwrap

load_dotenv()

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
API_KEY = os.getenv('YOUTUBE_API_KEY')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_youtube_service():
    if not API_KEY:
        print("ERROR: API Key tidak ditemukan. Silahkan masukan API Key Anda.")
        return None
    try:
        #Building the service object for YouTube
        youtube = build(
            API_SERVICE_NAME,
            API_VERSION,
            developerKey=API_KEY
        )
        return youtube
    except Exception as e:
        print(f"An error occured while creating the YouTube service: {e}")
        return None
    
def get_gemini_model():
    if not GEMINI_API_KEY:
        print("ERROR: Gemini API Key tidak ditemukan. Silahkan masukan API Key Anda.")
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        generation_config = {
            'temperature': 0.2,
            'top_p': 0.8,
            'top_k': 1,
        }
        model = GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config=generation_config
        )
        return model
    except Exception as e:
        print(f"An error occured while creating the Gemini service: {e}")
        return None
    
# This block is to search for videos based on the topic query
def search_youtube_videos(youtube_service, query, max_results=20):
    """
    Searches YouTube for videos based on a query.

    Args:
        youtube_service: The authenticated YouTube API service object.
        query (str): The search term (e.g., "python tutorial #shorts").
        max_results (int): The maximum number of search results to return.

    Returns:
        A list of dictionaries, where each dictionary contains 'title' and 'videoId'
        for a video, or None if an error occurs.
    """
    if not youtube_service:
        print("ERROR: YouTube service not available. Please check your API Key")
        return None
    
    try:
        search_response = youtube_service.search().list(
            q=query,
            part='snippet,id',
            type='video',
            order='relevance',
            maxResults=max_results,
            regionCode='ID',  # set the search region to Indonesia
        ).execute()

        videos = []
        
        for item in search_response.get('items', []):
            snippet_data = item.get('snippet', {})
            id_data = item.get('id', {})
            video_title = snippet_data.get('title', 'No Title')
            video_id = id_data.get('videoId', None)
            if video_id:
                # Append video details to the list
                videos.append({
                'title': video_title, 
                'videoId': video_id
                })
        return videos
    
    except Exception as e:
        print(f"An error occured while searching YouTube: {e}")
        return None

def get_video_details(youtube_service, video_ids):
    if not youtube_service:
        print("YouTube service is not available for fetching details.")
        return None
    if not video_ids:
        print("Video ID is required for fetching details.")
        return {}

    try:
        ids_strings = ','.join(video_ids)
        details_response = youtube_service.videos().list(
            id=ids_strings,
            part='snippet,statistics,contentDetails'
        ).execute()

        video_details = {}

        for item in details_response.get('items', []):
            video_id = item.get('id', None)

            if video_id: 

                stats = item.get('statistics', {})
                raw_view_count = stats.get('viewCount', 'N/A')
                raw_like_count = stats.get('likeCount', 'N/A')
                raw_comment_count = stats.get('commentCount', 'N/A')

                view_count = safe_int_convert(raw_view_count, default=0)
                like_count = safe_int_convert(raw_like_count, default=0)
                comment_count = safe_int_convert(raw_comment_count, default=0)

                if view_count > 0:
                    engagement_rate = round((like_count + comment_count) / view_count, 2)
                else:
                    engagement_rate = 'N/A'

                snippet = item.get('snippet', {})
                published_at_str = snippet.get('publishedAt', 'N/A')

                content_details = item.get('contentDetails', {})
                duration = content_details.get('duration', 'N/A')

                video_details[video_id] = {
                    'viewCount': view_count,
                    'publishedAt': published_at_str,
                    'duration': duration,
                    'likeCount': like_count,
                    'commentCount': comment_count,
                    'engagementRate': engagement_rate
                }

        return video_details

    except Exception as e:
        print(f"An error occured while fetching video details: {e}")
        return None
    
def safe_int_convert(value, default=0):
    try: return int(value)
    except (ValueError, TypeError): return default

def video_analysis (search_results, video_details):
    if not search_results or not video_details:
        print("No search results or video details provided.")
        return None
    
    analysis_summary = {
        'videos_data': []
    }

    for video_info in search_results:
        video_id = video_info.get('videoId')
        if not video_id:
            continue

        details = video_details.get(video_id, {})
        published_date = 'N/A'

        title = video_info.get('title', 'No Title')
        view_count_str = details.get('viewCount', 'N/A')
        duration = details.get('duration', 'N/A')
        published_at_str = details.get('publishedAt', 'N/A')

        current_engagement_rate_val = details.get('engagementRate', 'N/A')

        if published_at_str != 'N/A':

            try:
                published_datetime = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
                published_date = published_datetime.strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                published_date = published_at_str
        
        analysis_summary['videos_data'].append({
            'videoId': video_id,
            'duration': duration,
            'title': title,
            'viewCount': view_count_str,
            'publishedAt': published_date,
            'likeCount': details.get('likeCount', 'N/A'),
            'commentCount': details.get('commentCount', 'N/A'),
            'engagementRate': current_engagement_rate_val
        })

    total_views = 0
    valid_video_count = 0
    highest_views = 0
    total_engagement_sum = 0
    engagement_conntributed_video_count = 0

    analyzable_videos = []

    for video_data in analysis_summary['videos_data']:
        current_views = safe_int_convert(video_data.get('viewCount', 0))
        current_engagement_rate_val = video_data.get('engagementRate', 'N/A')
        
        if current_views > 0:
            total_views += current_views
            valid_video_count += 1
            if current_views > highest_views:
                highest_views = current_views
            analyzable_videos.append({
                'title': video_data['title'],
                'viewCount': current_views,
                'likeCount': video_data.get('likeCount', 'N/A'),
                'videoId': video_data['videoId'],
                'engagementRate': current_engagement_rate_val,
            })

        if isinstance(current_engagement_rate_val, (int, float)) and current_engagement_rate_val > 0:
            total_engagement_sum += current_engagement_rate_val
            engagement_conntributed_video_count += 1

    average_views = int(total_views / valid_video_count if valid_video_count > 0 else 0)

    average_engagement_rate = 0
    if engagement_conntributed_video_count > 0:
        average_engagement_rate = round(total_engagement_sum / engagement_conntributed_video_count, 2)

    top_performers = sorted(analyzable_videos, key=lambda x: x['viewCount'], reverse=True)[:5]

    analysis_summary['totalVideos'] = len(analysis_summary['videos_data'])
    analysis_summary['totalViews'] = total_views
    analysis_summary['averageViews'] = average_views
    analysis_summary['highestViews'] = highest_views
    analysis_summary['topPerformers'] = top_performers
    analysis_summary['averageEngagementRate'] = average_engagement_rate
    analysis_summary['currentTimeStamp'] = datetime.now().isoformat()

    return analysis_summary

def get_user_choice(prompt, options):
    while True:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        try:
            choice_int = int(input(f"\n {prompt} "))
            if 1 <= choice_int <= len(options):
                return choice_int
            else:
                print(f"Pilih antara nomor 1 dan {len(options)}.")
        except ValueError:
            print("Input tidak valid. Silakan masukkan nomor yang valid.")

if __name__ == '__main__':
    youtube_service = get_youtube_service()
    if youtube_service:
        print("Successfully connected to YouTube!")

        gemini_model =  get_gemini_model()
        if not gemini_model:
            print("Gemini model could not be created. Please check your API Key.")
            exit(1)

        search_query = input(f"\nSilakan masukkan topik ide konten yang ingin Anda validasi:\n(Contoh: 'misteri obyek interstellar', 'resep masakan sehat', 'fakta kota tua batavia')\nTopik: ").strip()

        print("\n--- Pilihan Filter ---")
        print("Apakah Anda ingin membatasi pencarian hanya pada video YouTube Shorts?")
        short_choice_options = ['Ya, hanya Shorts', 'Tidak, cari semua video relevan']

        short_choice = get_user_choice('Gunakan filter #shorts dalam pencarian?', short_choice_options)

        if short_choice == 1:
            search_query += " #shorts"

        print(f"\nMencari video dengan keyword: {search_query}")

        search_results = search_youtube_videos(youtube_service, search_query, max_results=20)

        if search_results:
            print(f"\nMenemukan {len(search_results)} video potensial (mengambil detail...)")

            video_ids_to_fetch = [video['videoId'] for video in search_results if video.get('videoId')]

            video_details = get_video_details(youtube_service, video_ids_to_fetch)

            # print(json.dumps(video_details, indent=2))

            if video_details:
                analysis_output = video_analysis(search_results, video_details)

                if analysis_output:
                    print("\n--- Memulai proses analisa... ---")
                    # print(json.dumps(analysis_output, indent=2))

                    top_videos = analysis_output.get('topPerformers', [])

                    if top_videos:
                        print(f"\n5 Video Teratas untuk pencarian {search_query}:")
                        for i, video in enumerate(top_videos, start=1):
                            views_formatted = f"{video.get('viewCount', 'N/A'):,}" if isinstance(video.get('viewCount'), (int, float)) else video.get('viewCount', 'N/A')
                            print(f"{i}. Judul: {video.get('title', 'N/A')}")
                            print(f"Penayangan: {views_formatted}")
                            print(f"Jumlah Suka: {video.get('likeCount', 'N/A')}")
                            print(f"Engagement Rate: {video.get('engagementRate', 'N/A')}")
                            print("-" * 20)
                        print(textwrap.dedent(f"""\
                        Catatan:
                        - Engagement Rate dihitung sebagai (Jumlah Suka + Jumlah Komentar) / Jumlah Penayangan
                        - Video dengan engagement rate yang lebih tinggi menunjukkan potensi yang lebih baik untuk ide konten Anda.
                        - Beberapa video mungkin tidak 100% relevan dengan topik Anda, namun tetap memiliki performa yang baik.
                        """))
                    else:
                        print("Tidak ada video yang memenuhi kriteria untuk analisis.")

                    channel_context_data = {
                    "subscriber_count": 47,
                        "top_videos": [
                            {"title": "Perpustakaan Terlarang di Vatikan", "views": "3200", "topic": "Sejarah & Misteri"},
                            {"title": "Misteri Garis Nasca: Teka-teki Raksasa di Padang Pasir", "views": "1800", "topic": "Misteri"},
                            {"title": "Olympus Mount: Gunung Terbesar di Tata Surya", "views": "1300", "topic": "Edutainment"}
                        ],
                        "target_audience": {
                            "age_range": "25-34",
                            "geography": "Indonesia, Malaysia",
                            "interests": "Sejarah, Misteri, Sains, dan Edutainment",
                            "gender_split": "Male 74%, Female 26%"
                        },
                        "niche": "Edutainment dan Misteri",
                        "total_views_365_days": 35000,
                        "content_type": "shorts"
                    }

                    llm_prompt = f"""
                    Anda adalah seorang ahli strategi pemasaran digital YouTube Shorts yang berpengalaman dan tajam.
                    Tugas Anda adalah menganalisis potensi ide konten yang disajikan dan memberikan rekomendasi yang jelas, singkat, dan langsung pada intinya.

                    Berikut adalah data analisis video Shorts terkait ide konten yang dicari. Data ini kini sangat kaya, mencakup detail per video seperti judul, ID, jumlah penayangan, tanggal publikasi, durasi, jumlah suka (likeCount), jumlah komentar (commentCount), dan tingkat keterlibatan (engagementRate). Ringkasan keseluruhan juga menyertakan rata-rata tingkat keterlibatan (averageEngagementRate). **Harap perhatikan juga 'currentTimestamp' yang menunjukkan waktu analisis dilakukan, untuk membantu Anda menilai usia video.**
                    {json.dumps(analysis_output, indent=2)}

                    ---
                    
                    Konteks channel YouTube saya untuk kebutuhan untuk analisis ini:
                    {json.dumps(channel_context_data, indent=2)}
                    
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

                    print("\n--- Menunggu hasil analisa oleh AI ---")
                    try:
                        gemini_response = gemini_model.generate_content(llm_prompt)
                        gemini_analysis_text = gemini_response.text
                        print("\n--- Hasil Analisa Konten ---")
                        print(gemini_analysis_text)
                    except Exception as e:
                        print(f"An error occurred while generating the analysis: {e}")
                        print("Please ensure your Gemini API key is correct and you have enough quota.")
                        gemini_analysis_text = None

                else:
                    print("No analysis output generated.")
            else:
                print("Failed to fetch video details.")
        else:
            print("No search results found.")
    else:
        print("YouTube service could not be created. Please check your API Key.")