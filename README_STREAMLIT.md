# YouTube Shorts Idea Analyzer

This is a Streamlit app that helps analyze YouTube Shorts content ideas by examining trending videos and providing insights using YouTube Data API and Google Gemini.

## How to Deploy to Streamlit Community Cloud

1. Create a new repository on GitHub with this code
2. Sign up for [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account to Streamlit
4. Select your repository when creating a new app
5. Set the main file as `app.py`
6. In the "Advanced settings" section, add your API keys as secrets:
   - `YOUTUBE_API_KEY`
   - `GEMINI_API_KEY`
7. Click "Deploy!"

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

## How to Use

1. Enter your YouTube Data API and Gemini API keys
2. Input your YouTube Shorts content idea
3. Click "Analyze Content Idea" and wait for the results
4. View the AI-generated analysis and recommendations