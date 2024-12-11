from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes required for the API
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Authenticate using OAuth2
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    credentials = flow.run_console()
    return build('youtube', 'v3', credentials=credentials)

# Initialize the YouTube API
youtube = get_authenticated_service()

# (Rest of your existing script remains the same)
