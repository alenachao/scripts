# Spotify Language Learning 🎵🌱
Given a language and your Spotify profile, create a playlist of songs that match your tastes and chosen language, helping you discover new music and learn a new language.
## Install requirements
```
pip install -r requirements.txt
```
## Configure Spotify API
Set up a [Spotify app](https://developer.spotify.com/documentation/web-api/concepts/apps). You will need to add `http://localhost:8888/callback` as a redirect uri
## Configure environment
create a `.env` in the same directory as the script will the following content, taken from your created spotify application:
```
CLIENT_ID = 'YOU_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
```
## Run it
Make sure your current directory is set to `spotify` 
```
python app.py <language>
```
Supported languages are based on the available genres Spotify has on its API. This includes: Cantonese, English, French, German, Hindi, Japanese, Korean, Malay, Mandarin, Persian, Portuguese, Spanish, Swedish, Tagalog, Turkish.\
Once you run the script, you should be directed to log into Spotify. Once you are redirected and the window says 'Tracks added successfully' you can close the tab and find the playlist in your Spotify library. \
\
![image](https://github.com/alenachao/scripts/assets/122919697/c18560d0-5b39-4087-aecf-536b40952b27)
