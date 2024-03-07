import os
import googleapiclient.discovery
import googleapiclient.errors
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def fetch_videos(api_key, channel_id):
  youtube = googleapiclient.discovery.build("youtube",
                                            "v3",
                                            developerKey=api_key)

  request = youtube.search().list(part="snippet",
                                  channelId=channel_id,
                                  maxResults=5,
                                  order="date")
  response = request.execute()

  return response['items']


def update_readme(videos):
  readme_path = "README.md"
  with open(readme_path, "r") as file:
    content = file.read()

  # Find the start and end markers
  start_marker = "<!-- YOUTUBE:START -->"
  end_marker = "<!-- YOUTUBE:END -->"
  start_index = content.find(start_marker)
  end_index = content.find(end_marker)

  if start_index == -1 or end_index == -1:
    print("Markers not found in README.md")
    return

  # Format the videos as cards with thumbnails and titles
  video_cards = []
  for video in videos:
    video_title = video['snippet']['title']
    video_id = video['id']['videoId']
    video_cards.append(
        f'<div class="video-card" style="width: 200px; border: 1px solid lightgray; border-radius: 10px; overflow: hidden;">'
        f'<a href="https://www.youtube.com/watch?v={video_id}">'
        f'<img src="https://img.youtube.com/vi/{video_id}/0.jpg" alt="{video_title}" width="200"/>'
        f'<p style="word-wrap: break-word; max-width: 100%; padding: 0 10px;">{video_title}</p>'
        f'</a>'
        f'</div>')
  new_content = "\n".join(video_cards)

  # Wrap the video cards in a grid container
  grid_container = f'<div class="video-grid" style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 20px;">{new_content}</div>'

  # Modify the content to include the video information between the markers
  content = content[:start_index + len(start_marker) +
                    1] + "\n" + grid_container + "\n" + content[end_index:]

  # Write the updated content back to the README.md file
  with open(readme_path, "w") as file:
    file.write(content)


def main():
  api_key = os.getenv(
      "YOUTUBE_API_KEY")  # Access the API key from the environment variable
  channel_id = os.getenv(
      "YOUTUBE_CHANNEL_ID"
  )  # Access the channel ID from the environment variable

  videos = fetch_videos(api_key, channel_id)
  update_readme(videos)


if __name__ == "__main__":
  main()
