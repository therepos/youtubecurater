from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Scopes required for the API
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Authenticate using OAuth2
def get_authenticated_service():
    if os.path.exists('token.json'):
        # Load existing credentials from token.json
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        # Authenticate using client_secret.json and save the token
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        credentials = flow.run_console()
        with open('token.json', 'w') as token_file:
            token_file.write(credentials.to_json())
    return build('youtube', 'v3', credentials=credentials)

# Initialize the YouTube API
youtube = get_authenticated_service()

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
def add_to_playlist(video_id, playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response

# Read songs from songs.txt
with open("songs.txt", "r") as file:
    songs = file.readlines()

# Playlist ID from environment variables
PLAYLIST_ID = os.environ["PLAYLIST_ID"]

# Process each song
for song in songs:
    song = song.strip()
    video_id = search_youtube(song)
    if video_id:
        add_to_playlist(video_id, PLAYLIST_ID)
        print(f"Added {song} to the playlist.")
    else:
        print(f"Could not find {song} on YouTube.")
