import os
import googleapiclient.discovery
import googleapiclient.errors
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def fetch_videos(api_key, channel_id):
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  request = youtube.search().list(
      part="snippet",
      channelId=channel_id,
      maxResults=5,
      order="date"
  )
  response = request.execute()

  return response['items']

def update_readme(videos):
    readme_path = "README.md"
    with open(readme_path, "r") as file:
        content = file.read()

    # Modify the content to include the video information in a card format
    new_content = "## Latest Videos\n\n"
    for video in videos:
        video_title = video['snippet']['title']
        video_id = video['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_thumbnail = video['snippet']['thumbnails']['default']['url']
        new_content += f"""
        <a href="{video_url}" target="_blank">
            <img src="{video_thumbnail}" alt="{video_title}" width="200" height="113">
        </a>
        <h3><a href="{video_url}" target="_blank">{video_title}</a></h3>
        """

    content = new_content + "\n" + content

    with open(readme_path, "w") as file:
        file.write(content)

def main():
  api_key = os.getenv("YOUTUBE_API_KEY") # Access the API key from the environment variable
  channel_id = os.getenv("YOUTUBE_CHANNEL_ID") # Access the channel ID from the environment variable

  videos = fetch_videos(api_key, channel_id)
  update_readme(videos)

if __name__ == "__main__":
  main()