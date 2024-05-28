import os
from dotenv import load_dotenv
import requests
import base64
import json

load_dotenv()
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def getAccessToken(): 
    auth = str(base64.b64encode((client_id + ":" + client_secret).encode('utf-8')), 'utf-8')
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic' + auth,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    
    result = requests.post(url, headers=headers, data=data)
    token = json.loads(result.content)['access_token']
    
    return token

def main():
    
    # http GET 'https://api.spotify.com/v1/me/following?type=artist' \
    # Authorization:'Bearer 1POdFZRZbvb...qqillRxMr2z'

    return

if __name__ == "__main__":
  main()