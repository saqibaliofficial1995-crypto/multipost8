import os
import time
import requests

REQUIRED_ENV_VARS = [
    "YT_CLIENT_ID",
    "YT_CLIENT_SECRET",
    "YT_REFRESH_TOKEN",
    "DRIVE_REFRESH_TOKEN",
    "DRIVE_FOLDER_ID",
    "GEMINI_API_KEY"
]

YOUTUBE_SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
]

DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive'
]

def validate_env(service=None):
    if service == "youtube":
        reqs = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
    elif service == "drive":
        reqs = ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "DRIVE_REFRESH_TOKEN"]
    else:
        reqs = REQUIRED_ENV_VARS
        
    missing = [v for v in reqs if not os.environ.get(v)]
    if missing:
        raise ValueError(f"Missing required environment variable(s): {', '.join(missing)}")

def _refresh_oauth_token(refresh_token_env_var, scopes=None):
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get(refresh_token_env_var)

    if not client_id or not client_secret or not refresh_token:
        raise ValueError(f"Missing OAuth credentials: check YT_CLIENT_ID, YT_CLIENT_SECRET, and {refresh_token_env_var}.")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    if scopes:
        data["scope"] = " ".join(scopes)

    for attempt in range(5):
        try:
            res = requests.post(token_url, data=data, timeout=20)
            if res.status_code == 200:
                return res.json()["access_token"]
            elif res.status_code in [400, 401]:
                raise RuntimeError(f"OAuth token refresh rejected: {res.status_code} {res.text}")
        except requests.exceptions.RequestException:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Failed to refresh OAuth token for {refresh_token_env_var} after multiple attempts.")

def get_youtube_credentials():
    """Returns refreshed YouTube access token for Historiana brand account."""
    validate_env(service="youtube")
    return _refresh_oauth_token("YT_REFRESH_TOKEN", YOUTUBE_SCOPES)

def get_drive_credentials():
    """Returns refreshed Drive access token for primary Google account."""
    validate_env(service="drive")
    return _refresh_oauth_token("DRIVE_REFRESH_TOKEN", DRIVE_SCOPES)

# Convenience aliases
get_youtube_token = get_youtube_credentials
get_drive_token = get_drive_credentials

def get_access_token():
    """Backwards-compatible helper returning YouTube credentials."""
    return get_youtube_credentials()

def get_gemini_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is not set.")
    return key

def get_drive_folder_id():
    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    if not folder_id:
        raise ValueError("DRIVE_FOLDER_ID is not set.")
    return folder_id
