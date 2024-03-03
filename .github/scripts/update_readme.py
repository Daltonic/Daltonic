import json
import os

def update_readme():
    # Path to the JSON file containing the latest videos
    latest_videos_path = "latest_videos.json"
    # Path to the README.md file
    readme_path = "README.md"

    # Load the latest videos from the JSON file
    with open(latest_videos_path, "r") as file:
        videos = json.load(file)

    # Read the current content of README.md
    with open(readme_path, "r") as file:
        content = file.read()

    # Prepare the new content to be added to README.md
    new_content = "## Latest Videos\n\n"
    for video in videos:
        new_content += f"- [{video['snippet']['title']}](https://www.youtube.com/watch?v={video['id']['videoId']})\n"

    # Update the README.md content
    content = new_content + "\n" + content

    # Write the updated content back to README.md
    with open(readme_path, "w") as file:
        file.write(content)

    # Clean up the latest_videos.json file
    os.remove(latest_videos_path)

if __name__ == "__main__":
    update_readme()