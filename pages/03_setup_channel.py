import streamlit as st
from googleapiclient.discovery import build

# Function to fetch channel information using YouTube API
def fetch_channel_info(api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # For API key-only access, we need to search for the channel first
        # This approach requires the user to know their channel name or ID
        st.info("ℹ️ To auto-fetch channel information, please enter your channel name or ID below:")
        channel_identifier = st.text_input("Channel Name or ID", placeholder="e.g., @YourChannelName or UCXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        
        if not channel_identifier:
            return None
            
        # Try to find channel by username/handle first
        if channel_identifier.startswith('@'):
            # Handle format (new YouTube format)
            search_response = youtube.search().list(
                part='snippet',
                type='channel',
                q=channel_identifier,
                maxResults=1
            ).execute()
        else:
            # Try as channel ID or name
            try:
                # First try as channel ID
                channel_response = youtube.channels().list(
                    part='snippet,statistics',
                    id=channel_identifier
                ).execute()
                if channel_response.get('items'):
                    search_response = channel_response
                else:
                    # If that fails, search by name
                    search_response = youtube.search().list(
                        part='snippet',
                        type='channel',
                        q=channel_identifier,
                        maxResults=1
                    ).execute()
            except:
                # Fallback to search
                search_response = youtube.search().list(
                    part='snippet',
                    type='channel',
                    q=channel_identifier,
                    maxResults=1
                ).execute()
        
        if not search_response.get('items'):
            st.warning("⚠️ Could not find channel with that identifier. Please check and try again.")
            return None
            
        channel_item = search_response['items'][0]
        channel_id = channel_item['id']['channelId'] if 'channelId' in channel_item['id'] else channel_item['id']
        
        # Get detailed channel statistics
        channel_response = youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()
        
        if not channel_response.get('items'):
            return None
            
        channel_data = channel_response['items'][0]
        
        # Extract relevant information
        snippet = channel_data.get('snippet', {})
        statistics = channel_data.get('statistics', {})
        
        channel_info = {
            'id': channel_id,
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'subscriber_count': int(statistics.get('subscriberCount', 0)),
            'view_count': int(statistics.get('viewCount', 0)),
            'video_count': int(statistics.get('videoCount', 0)),
            'country': snippet.get('country', ''),
        }
        
        return channel_info
    except Exception as e:
        st.error(f"Error fetching channel info: {str(e)}")
        return None

# Function to fetch top videos for the channel
def fetch_top_videos(api_key, channel_id=None):
    try:
        if not channel_id:
            st.warning("⚠️ Channel ID is required to fetch top videos. Please enter your channel information first.")
            return []
            
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Get top videos sorted by view count
        search_response = youtube.search().list(
            channelId=channel_id,
            part='snippet,id',
            type='video',
            order='viewCount',
            maxResults=3
        ).execute()
        
        top_videos = []
        video_ids = [item['id']['videoId'] for item in search_response.get('items', []) if item.get('id', {}).get('videoId')]
        
        if video_ids:
            # Get detailed video statistics
            videos_response = youtube.videos().list(
                id=','.join(video_ids),
                part='snippet,statistics'
            ).execute()
            
            for item in videos_response.get('items', []):
                snippet = item.get('snippet', {})
                statistics = item.get('statistics', {})
                
                top_videos.append({
                    'title': snippet.get('title', ''),
                    'views': statistics.get('viewCount', '0'),
                    'topic': 'Your Top Video',  # We'll let users customize this
                })
        
        return top_videos
    except Exception as e:
        st.error(f"Error fetching top videos: {str(e)}")
        return []

st.set_page_config(
    page_title="Setup Channel Context - YouTube Shorts Idea Analyzer",
    page_icon="📺",
    layout="centered"
)

st.title("📺 Setup Channel Context")

st.markdown("""
Atur konteks channel YouTube kamu untuk membuat analisis lebih akurat dan relevan dengan channel kamu.
Informasi ini akan digunakan oleh AI untuk memberikan rekomendasi yang lebih tepat sasaran.

ℹ️ **Catatan**: Data default di bawah ini hanyalah contoh. Harap ganti dengan informasi channel kamu sendiri untuk hasil yang lebih akurat.
""")

# Auto-fetch channel information if API keys are available
if st.session_state.get('yt_api_key'):
    st.info("ℹ️ To auto-fetch channel information, please enter your channel name or ID below:")
    channel_identifier = st.text_input("Channel Name or ID", placeholder="e.g., @YourChannelName or UCXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", key="channel_identifier")
    
    if st.button("🔍 Auto-fetch Channel Information") and channel_identifier:
        with st.spinner("Fetching channel information..."):
            channel_info = fetch_channel_info(st.session_state['yt_api_key'])
            if channel_info:
                # Update session state with fetched information
                st.session_state.channel_context.update({
                    "subscriber_count": channel_info['subscriber_count'],
                    "total_views_365_days": channel_info['view_count'],  # Approximation
                    "niche": "Please specify your niche",  # We can't determine this automatically
                })
                st.success("✅ Channel information fetched successfully!")
                st.info("Please review and complete the information below, especially the audience details and niche.")
                
                # Try to fetch top videos
                top_videos = fetch_top_videos(st.session_state['yt_api_key'], channel_info['id'])
                if top_videos:
                    st.session_state.channel_context["top_videos"] = top_videos
                    st.success("✅ Top videos fetched successfully!")
            else:
                st.warning("⚠️ Could not fetch channel information. Please check your channel identifier or enter information manually.")
else:
    st.info("ℹ️ Set up your API keys first in the 'Setup API Keys' page to enable auto-fetching of channel information.")

# Initialize session state for channel context if not already present
# Using generic placeholder data that users should customize
if 'channel_context' not in st.session_state:
    st.session_state.channel_context = {
        "subscriber_count": 0,
        "top_videos": [
            {"title": "Video pertama kamu", "views": "0", "topic": "Topik video"},
            {"title": "Video kedua kamu", "views": "0", "topic": "Topik video"},
            {"title": "Video ketiga kamu", "views": "0", "topic": "Topik video"}
        ],
        "target_audience": {
            "age_range": "Contoh: 18-24, 25-34",
            "geography": "Contoh: Indonesia, Jakarta",
            "interests": "Contoh: Teknologi, Hiburan, Edukasi",
            "gender_split": "Contoh: Male 60%, Female 40%"
        },
        "niche": "Contoh: Edutainment, Gaming, Kuliner",
        "total_views_365_days": 0,
        "content_type": "shorts"
    }

# Create form for channel context entry
with st.form("channel_context_form"):
    st.subheader("📊 Informasi Channel")
    
    col1, col2 = st.columns(2)
    with col1:
        subscriber_count = st.number_input(
            "Jumlah Subscriber", 
            value=st.session_state.channel_context["subscriber_count"],
            min_value=0,
            help="Jumlah subscriber channel kamu saat ini"
        )
    with col2:
        total_views_365_days = st.number_input(
            "Total Penayangan (365 hari)", 
            value=st.session_state.channel_context["total_views_365_days"],
            min_value=0,
            help="Total penayangan dalam 365 hari terakhir"
        )
    
    niche = st.text_input(
        "Niche Channel", 
        value=st.session_state.channel_context["niche"],
        help="Niche utama channel kamu (contoh: Edutainment, Gaming, Kuliner)"
    )
    
    st.subheader("👥 Target Audience")
    
    col1, col2 = st.columns(2)
    with col1:
        age_range = st.text_input(
            "Rentang Usia", 
            value=st.session_state.channel_context["target_audience"]["age_range"],
            help="Rentang usia utama penonton kamu (contoh: 18-24, 25-34)"
        )
    with col2:
        geography = st.text_input(
            "Wilayah Geografis", 
            value=st.session_state.channel_context["target_audience"]["geography"],
            help="Wilayah geografis utama penonton kamu (contoh: Indonesia, Jakarta)"
        )
    
    interests = st.text_input(
        "Minat & Ketertarikan", 
        value=st.session_state.channel_context["target_audience"]["interests"],
        help="Minat utama penonton kamu (contoh: Teknologi, Hiburan, Edukasi)"
    )
    
    gender_split = st.text_input(
        "Pembagian Gender", 
        value=st.session_state.channel_context["target_audience"]["gender_split"],
        help="Pembagian gender penonton (contoh: Male 60%, Female 40%)"
    )
    
    st.subheader("🏆 Top 3 Videos (Direkomendasikan)")
    st.markdown("Masukkan informasi tentang 3 video terbaik kamu untuk membantu AI memahami konten kamu dan memberikan rekomendasi yang lebih akurat. Ini sangat membantu AI dalam menganalisis potensi ide konten baru.")
    
    top_videos = []
    for i in range(3):
        st.markdown(f"**Video #{i+1}**")
        col1, col2, col3 = st.columns(3)
        with col1:
            title = st.text_input(f"Judul Video #{i+1}", 
                                value=st.session_state.channel_context["top_videos"][i]["title"] if i < len(st.session_state.channel_context["top_videos"]) else "",
                                placeholder="Contoh: 5 Fakta Misteri Yang Belum Terpecahkan",
                                key=f"title_{i}")
        with col2:
            views = st.text_input(f"Penayangan #{i+1}", 
                                value=st.session_state.channel_context["top_videos"][i]["views"] if i < len(st.session_state.channel_context["top_videos"]) else "",
                                placeholder="Contoh: 10000",
                                key=f"views_{i}")
        with col3:
            topic = st.text_input(f"Topik #{i+1}", 
                                value=st.session_state.channel_context["top_videos"][i]["topic"] if i < len(st.session_state.channel_context["top_videos"]) else "",
                                placeholder="Contoh: Misteri Dunia",
                                key=f"topic_{i}")
        
        if title and views and topic:
            top_videos.append({
                "title": title,
                "views": views,
                "topic": topic
            })
    
    submitted = st.form_submit_button("Simpan Informasi Channel")
    
    if submitted:
        # Update session state with new channel context
        st.session_state.channel_context = {
            "subscriber_count": subscriber_count,
            "top_videos": top_videos if top_videos else st.session_state.channel_context["top_videos"],
            "target_audience": {
                "age_range": age_range,
                "geography": geography,
                "interests": interests,
                "gender_split": gender_split
            },
            "niche": niche,
            "total_views_365_days": total_views_365_days,
            "content_type": "shorts"
        }
        st.success("✅ Informasi channel berhasil disimpan!")
        st.info("Sekarang kamu bisa masuk ke halaman 'Analisis Ide Konten' untuk menggunakan informasi channel ini.")

# Information about how this data is used
st.markdown("---")
st.subheader("ℹ️ Cara Data Ini Digunakan")

st.markdown("""
Data channel kamu digunakan untuk:

1. **Personalisasi Rekomendasi**: AI akan memberikan rekomendasi yang sesuai dengan niche dan audiens kamu
2. **Analisis Kompetitif**: Membandingkan potensi ide konten dengan performa video kamu sebelumnya
3. **Strategi Konten**: Memberikan saran yang relevan dengan gaya dan topik yang sudah kamu kuasai

📋 **Mengapa Top 3 Videos Penting**:
Informasi tentang video terbaik kamu sangat membantu AI untuk:
- Memahami jenis konten yang berhasil di channel kamu
- Mengidentifikasi pola dan elemen yang menarik bagi audiens kamu
- Memberikan rekomendasi yang sesuai dengan gaya konten kamu

🔒 **Privasi**: Data ini hanya disimpan di session browser kamu dan tidak akan dikirim ke server manapun.

⚠️ **Penting**: Data default yang ditampilkan hanyalah contoh. Harap masukkan data channel kamu sendiri untuk hasil analisis yang akurat.
""")