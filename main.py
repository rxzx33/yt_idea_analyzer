# Main functions for YouTube Shorts Analyzer
from googleapiclient.discovery import build
import google.generativeai as genai
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
from datetime import datetime
import json
import os
import textwrap
import math

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
def search_youtube_videos(youtube_service, query, max_results=30):
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
            regionCode='ID'  # Hardcode to Indonesia
        ).execute()

        videos = []
        
        # Convert query to lowercase for case-insensitive comparison
        query_terms = [term.lower() for term in query.replace("#shorts", "").strip().split() if term]
        
        for item in search_response.get('items', []):
            snippet_data = item.get('snippet', {})
            id_data = item.get('id', {})
            video_title = snippet_data.get('title', 'No Title')
            video_id = id_data.get('videoId', None)
            if video_id:
                # Check if the video is relevant by ensuring query terms appear in title
                title_lower = video_title.lower()
                is_relevant = True
                
                # For non-shorts searches, we want to be more strict about relevance
                if "#shorts" not in query and query_terms:
                    is_relevant = any(term in title_lower for term in query_terms)
                
                # Append video details to the list if relevant
                if is_relevant:
                    videos.append({
                    'title': video_title, 
                    'videoId': video_id,
                    'url': f'https://www.youtube.com/watch?v={video_id}'
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
            'url': f'https://www.youtube.com/watch?v={video_id}',
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

    # Calculate a relevance score that combines views and engagement
    # This gives better results than sorting by view count alone
    for video_data in analysis_summary['videos_data']:
        current_views = safe_int_convert(video_data.get('viewCount', 0))
        current_engagement_rate_val = video_data.get('engagementRate', 'N/A')
        
        if current_views > 0:
            total_views += current_views
            valid_video_count += 1
            if current_views > highest_views:
                highest_views = current_views
            
            # Calculate a composite score for ranking
            # Using log of views to prevent extremely popular videos from dominating
            # and engagement rate to ensure quality content is prioritized
            # Additive approach to balance views and engagement more effectively
            views_score = math.log10(current_views + 1) if current_views > 0 else 0
            engagement_score = current_engagement_rate_val if isinstance(current_engagement_rate_val, (int, float)) else 0
            # Convert engagement rate to a 0-10 scale and add to views score
            engagement_bonus = engagement_score * 100  # Convert percentage to 0-10 scale
            composite_score = views_score + engagement_bonus
            
            analyzable_videos.append({
                'title': video_data['title'],
                'viewCount': current_views,
                'likeCount': video_data.get('likeCount', 'N/A'),
                'videoId': video_data['videoId'],
                'engagementRate': current_engagement_rate_val,
                'url': video_data.get('url', f'https://www.youtube.com/watch?v={video_data["videoId"]}'),
                'compositeScore': composite_score
            })

        if isinstance(current_engagement_rate_val, (int, float)) and current_engagement_rate_val > 0:
            total_engagement_sum += current_engagement_rate_val
            engagement_conntributed_video_count += 1

    average_views = int(total_views / valid_video_count if valid_video_count > 0 else 0)

    average_engagement_rate = 0
    if engagement_conntributed_video_count > 0:
        average_engagement_rate = round(total_engagement_sum / engagement_conntributed_video_count, 2)

    # Sort by composite score instead of just view count for better relevance
    top_performers = sorted(analyzable_videos, key=lambda x: x['compositeScore'], reverse=True)[:5]

    analysis_summary['totalVideos'] = len(analysis_summary['videos_data'])
    analysis_summary['totalViews'] = total_views
    analysis_summary['averageViews'] = average_views
    analysis_summary['highestViews'] = highest_views
    analysis_summary['topPerformers'] = top_performers
    analysis_summary['averageEngagementRate'] = average_engagement_rate
    analysis_summary['currentTimeStamp'] = datetime.now().isoformat()

    return analysis_summary
