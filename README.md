[![Try on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ytshortsanalyze.streamlit.app)

# YouTube Video Idea Analyzer

> **Note:** The user interface for this application is in **Bahasa Indonesia**.

A Streamlit web application that helps content creators analyze the potential of their video ideas before production. By providing a topic, the app fetches data for similar videos on YouTube and uses a generative AI model to provide insights on demand, competition, and relevance.

## Features

- **Demand Analysis:** See if your video idea has the potential to get a high number of views based on existing similar content.
- **Competition Analysis:** Understand how many other creators are making similar content.
- **Content Suggestions:** Get recommendations on how to tailor your content based on the analysis.
- **YouTube Shorts Filter:** Optionally limit your analysis to only YouTube Shorts.

## How to Use

To run this application locally, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rxzx33/yt_idea_analyzer.git
    cd yt_idea_analyzer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Keys:**
    This application requires you to have your own API keys for the YouTube Data API and the Google Generative AI (Gemini) API.

    -   Create a file named `.env` in the root of the project directory.
    -   Add your API keys to the `.env` file in the following format:
        ```
        YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY_HERE"
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
        ```

5.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application should now be open in your web browser.

## Technologies Used

- **Python**
- **Streamlit:** For the web application interface.
- **Google API Python Client:** To interact with the YouTube Data API v3.
- **Google Generative AI:** For content analysis and recommendations.
