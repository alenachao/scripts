import os
from dotenv import load_dotenv
import requests
import base64
import json
import argparse
from flask import Flask, redirect, request, url_for, jsonify
import urllib
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

load_dotenv()
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
redirect_uri = 'http://localhost:8888/callback'
access_token = None

language_to_genre = {
    "portuguese":"brazil", 
    "cantonese":"cantopop", 
    "french":"french", 
    "german":"german", 
    "hindi":"indian", 
    "persian":"iranian", 
    "japanese":"j-pop",
    "korean":"k-pop",
    "malay":"malay",
    "mandarin":"mandopop", 
    "tagalog":"philippines-opm", 
    "spanish":"spanish", 
    "swedish":"swedish", 
    "turkish":"turkish",
    "english":"pop"
}

language_to_market = {
    "portuguese": "BR",  # Brazil
    "cantonese": "HK",   # Hong Kong
    "french": "FR",      # France
    "german": "DE",      # Germany
    "hindi": "IN",       # India
    "persian": "US",     # Iran not available
    "japanese": "JP",    # Japan
    "korean": "KR",      # South Korea
    "malay": "MY",       # Malaysia
    "mandarin": "US",    # China notavailable
    "tagalog": "PH",     # Philippines
    "spanish": "ES",     # Spain
    "swedish": "SE",     # Sweden
    "turkish": "TR",     # Turkey
    "english": "US"      # USA
}

# user authentication
@app.route('/')
def login():
    '''
    https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    '''
    state = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8').rstrip('=')
    query_params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'playlist-modify-public playlist-modify-private user-top-read',
        'redirect_uri': redirect_uri,
        'state': state
    }
    auth_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)
    return redirect(auth_url)

# get access token
@app.route('/callback')
def callback(): 
    '''
    https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    '''
    global access_token
    
    try:
        state = request.args.get('state')
        if not state:
            raise ValueError('State mismatch error')
        
        code = request.args.get('code')
        auth = str(base64.b64encode((client_id + ":" + client_secret).encode('utf-8')), 'utf-8')
        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + auth,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code
        }
        
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        access_token = json.loads(response.content)['access_token']
        print('successfully authenticated with spotify')
        
        return redirect(url_for('create_playlist'))
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/create_playlist')
def create_playlist():
    '''
    https://developer.spotify.com/documentation/web-api/reference/create-playlist
    https://developer.spotify.com/documentation/web-api/reference/add-tracks-to-playlist
    '''
    user_tracks = get_tracks()
    recs = get_recs(user_tracks)
    user_id = get_id()

    # create playlist
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    data = {
        'name': f'meep ({language} ver.)',
        'description': 'moop',
        'public': False
    }
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()

    playlist = json.loads(response.content)
    playlist_id = playlist['id']
    print(f"Playlist created: {playlist['name']}")

    # add to playlist
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    data = {
        'uris': [f"spotify:track:{track['id']}" for track in recs]
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return 'Tracks added successfully'

'''
helper functions
'''

# get user's top tracks
def get_tracks():
    '''
    https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
    '''
    url = 'https://api.spotify.com/v1/me/top/tracks?limit=2'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
        
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    tracks = json.loads(response.content)['items']
    print("successfully fetched user's top tracks")
    return tracks

# get recommendations
def get_recs(tracks):
    '''
    https://developer.spotify.com/documentation/web-api/reference/get-recommendations
    '''
    print("DEBUG: " + str(tracks))
    seed_tracks = ','.join([track['id'] for track in tracks])
    url = f'https://api.spotify.com/v1/recommendations?market={language_to_market[language]}&seed_genres={language_to_genre[language]}&seed_tracks={seed_tracks}&target_popularity=80'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    recommendations = json.loads(response.content)['tracks']
    print('successfully fetched recommended tracks')
    return recommendations

# get users spotify id
def get_id():
    '''
    https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    '''
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    user_id = json.loads(response.content)['id']
    print("successfully fetched user id")
    return user_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Making Spotify playlist based on your language of choice")
    parser.add_argument("language", type=str, help="supported languages: Cantonese, English, French, German, Hindi, Japanese, Korean, Malay, Mandarin, Persian, Portuguese, Spanish, Swedish, Tagalog, Turkish")

    args = parser.parse_args()
    language = str.lower(args.language)

    webbrowser.open('http://127.0.0.1:8888')

    app.run(port=8888)