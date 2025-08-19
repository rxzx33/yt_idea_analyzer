# YouTube Shorts Idea Analyzer

This application helps analyze YouTube Shorts content ideas by examining trending videos and providing insights using YouTube Data API and Google Gemini.

## Multi-Page Interface

This application now features a multi-page interface for better user experience:

1. **Home Page** - Overview and instructions (now includes content analysis)
2. **Setup Channel Context** - Enter information about your YouTube channel for personalized analysis (uses generic placeholders by default)
3. **Setup API Keys** - Securely enter and store your API keys

## Important Note About API Keys

This application requires you to provide your own API keys for:
1. YouTube Data API - to search for and analyze YouTube videos
2. Google Gemini API - to generate content recommendations

Your API keys are stored locally in your browser session and are never sent to any server, ensuring that API costs are associated with your own account.

## Cara Menggunakan Aplikasi Ini

1. Dapatkan kunci API YouTube Data API dan Google Gemini API Anda (instruksi di bawah)
2. Navigasi ke halaman "Setup API Keys" di sidebar
3. Masukkan dan simpan kunci API Anda (akan disimpan di sesi browser Anda)
4. Navigasi ke halaman "Setup Channel Context" di sidebar
5. Masukkan dan simpan informasi channel Anda untuk analisis yang dipersonalisasi (termasuk 3 Video Teratas Anda)
6. Kembali ke halaman utama (Home Page)
7. Masukkan ide konten YouTube Shorts Anda di kolom teks
8. Pilih apakah akan memfilter hasil hanya untuk konten Shorts
9. Klik "Analisa Ide Konten"
10. Tunggu analisis selesai
11. Lihat rekomendasi dan wawasan yang dihasilkan AI

⚠️ **Important**: 
- Both API Keys and Channel Context must be set up before you can perform content analysis
- For best results, complete the Top 3 Videos information in your channel context

## Getting API Keys

### YouTube Data API
1. Visit the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Copy the API key

### Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Navigate to "Get API key in Google Cloud"
4. Create and copy your API key

## Privacy & Data Security

This application prioritizes your privacy:

- **No Server Storage**: All data (API keys, channel context) is stored locally in your browser session
- **Generic Placeholders**: Default channel data uses generic placeholders, not real user data
- **No Tracking**: The application does not track or collect any personal information
- **Transparent**: All data handling is clearly explained in the application

## Deploying to Streamlit Community Cloud

If you want to deploy this application yourself:

1. Fork this repository
2. Sign up for [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account to Streamlit
4. Select your repository when creating a new app
5. Set the main file as `app.py`
6. Click "Deploy!"

## Local Development

To run this app locally:

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. Navigate between pages using the sidebar