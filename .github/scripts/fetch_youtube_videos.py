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

  # Modify the content to include the video information
  # This is a simple example; you'll need to adjust it based on your README structure
  new_content = "## Latest Videos\n\n"
  for video in videos:
      new_content += f"- [{video['snippet']['title']}](https://www.youtube.com/watch?v={video['id']['videoId']})\n"

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