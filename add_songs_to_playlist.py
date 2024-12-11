import os
from googleapiclient.discovery import build

# Get API key and playlist ID from environment variables
API_KEY = os.environ["AIzaSyDJ-Otd9FrQmaA6BqHh-lio8XtwWNt46fQ"]
PLAYLIST_ID = os.environ["PLHdjYV9dT0NwUO7jU4JWTmJKA-YxeuUim"]

# Initialize the YouTube API
youtube = build("youtube", "v3", developerKey=API_KEY)

# Function to search for a song on YouTube and get the video ID
def search_youtube(song):
    request = youtube.search().list(
        q=song,
        part="snippet",
        maxResults=1,
        type="video"
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["id"]["videoId"]
    return None

# Function to add a video to the playlist
def add_to_playlist(video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": PLAYLIST_ID,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

# Read songs from the songs.txt file in the repository
with open("songs.txt", "r") as file:
    songs = file.readlines()

# Process each song
for song in songs:
    song = song.strip()
    video_id = search_youtube(song)
    if video_id:
        add_to_playlist(video_id)
        print(f"Added {song} to the playlist.")
    else:
        print(f"Could not find {song} on YouTube.")
