# YouTube Shorts Idea Analyzer

This application helps analyze YouTube Shorts content ideas by examining trending videos and providing insights using YouTube Data API and Google Gemini.

## Important Note About API Keys

This application requires you to provide your own API keys for:
1. YouTube Data API - to search for and analyze YouTube videos
2. Google Gemini API - to generate content recommendations

You'll need to enter these keys each time you use the application. This ensures that API costs are associated with your own account rather than the app owner's account.

## How to Use This Application

1. Get your YouTube Data API and Google Gemini API keys (instructions below)
2. Enter your API keys in the application interface
3. Input your YouTube Shorts content idea in the text field
4. Choose whether to filter results for Shorts content only
5. Click "Analisa Ide Konten" (Analyze Content Idea)
6. Wait for the analysis to complete
7. View the AI-generated recommendations and insights

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

## Deploying to Streamlit Community Cloud

If you want to deploy this application yourself:

1. Fork this repository
2. Sign up for [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account to Streamlit
4. Select your repository when creating a new app
5. Set the main file as `app.py`
6. Click "Deploy!"
7. When using the app, you'll still need to enter your own API keys each time

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
4. Enter your API keys when prompted