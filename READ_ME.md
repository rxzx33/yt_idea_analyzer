# YouTube Shorts Idea Analyzer

This application helps analyze YouTube Shorts content ideas by examining trending videos and providing insights using YouTube Data API and Google Gemini.

## Multi-Page Interface

This application now features a multi-page interface for better user experience:

1. **Home Page** - Overview and instructions
2. **Setup Channel Context** - Enter information about your YouTube channel for personalized analysis (uses generic placeholders by default)
3. **Setup API Keys** - Securely enter and store your API keys
4. **Analyze Content** - Perform content analysis using your API keys and channel context

## Important Note About API Keys

This application requires you to provide your own API keys for:
1. YouTube Data API - to search for and analyze YouTube videos
2. Google Gemini API - to generate content recommendations

Your API keys are stored locally in your browser session and are never sent to any server, ensuring that API costs are associated with your own account.

## How to Use This Application

1. Get your YouTube Data API and Google Gemini API keys (instructions below)
2. Navigate to the "Setup API Keys" page
3. Enter and save your API keys (they'll be stored in your browser session)
4. Go to the "Analyze Content" page
5. Input your YouTube Shorts content idea in the text field
6. Choose whether to filter results for Shorts content only
7. Click "Analisa Ide Konten" (Analyze Content Idea)
8. Wait for the analysis to complete
9. View the AI-generated recommendations and insights

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