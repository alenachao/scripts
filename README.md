# Random Scripts ⚙️
A soon to be collection of scripts to hopefully automate my life a bit. 
<br><br>
For all scripts you will need to clone the repo. For SSH:
```
git clone git@github.com:alenachao/scripts.git
```

# Google Calendar Upload 🗓️ 
Given a CSV file of google calendar events, add them all to the user's Google Calendar.
## Install requirements
```
pip install -r requirements.txt
```
## Configure Google Authorization and APIs
1. Registration:
  - Register for [Google Cloud](https://console.cloud.google.com/)
  - Create a new project and name it whatever you want
2. Enable Calendar API:
  - Within the new project, go to APIs & Serivices > Enabled APIs & Services > Click Enable APIs & Services > Search for and enable the Google Calendar API
3. Configure OAuth Consent Screen (What shows up when user logs in):
  - Go back to APIs & Serivices > OAuth Consent Screen > Select External Users > Name the project again (same name is okay) > Enter user support email (doesn't matter too much) > Leave defaults > Add test users if you'd like (I suggest putting your own email for testing)
4. Set up Client Credentials:
  - Go back > Credentials > Click Create Credentials > Select OAuth Client ID > Select web application > Make redirect uri http://localhost:3000
  - Download the credentials JSON file and put it in the same directory as `app.py`, naming it `credentials.json`
## Write Your CSV File
Each row will be an event instance and each column will be an attribute of the event. Supported attributes:
| Attribute | Required/Default Value | Description | Type | Example |
|---|---|---|---|---|
| summary | REQUIRED | Name of the event | String | Google I/O 2015 |
| location | Nothing | Location of the event | String | 800 Howard St., San Francisco, CA 94103 |
| description | Nothing | Description of the event | String | A chance to hear more about Google\'s developer products. |
| start.dateTime | REQUIRED | Start date and time of the event | String in RFC3339 format | S2024-01-10T09:00:00-07:00 |
| start.timeZone | UTC | Time zone of start time | String | America/Los_Angeles |
| end.dateTime | REQUIRED | End date and time of the event | String in RFC3339 format | 2024-01-10T17:00:00-07:00 |
| end.timeZone | UTC | Time zone of start time | String | America/Los_Angeles |
| attendees | Nothing | List of attendees | Comma separated list | lpage@example.com,sbrin@example.com |
| recurrence | Nothing | List of recurance rules | Comma separated list | RRULE:FREQ=DAILY;COUNT=2 |

You spreadsheet should look something like this:
| summary	| location | description	| start.dateTime |	end.dateTime |	start.timeZone |	end.timeZone |	attendees |	recurrence |
|---|---|---|---|---|---|---|---|---|
| Google I/O 2015	| 800 Howard St., San Francisco, CA 94103	| A chance to hear more about Google\'s developer products.	| 2024-01-10T09:00:00-07:00	 | 2024-01-10T17:00:00-07:00 |	America/Los_Angeles |	America/Los_Angeles |	lpage@example.com,sbrin@example.com	 | RRULE:FREQ=DAILY;COUNT=2

Put the csv file in the same directory as `app.py` and name it `events.py`

## Run it
```
cd google_calendar
python3 app.py
```
Note you will only have to login the first time due to the token.json file, delete that file it you wanna relogin :)

## Future Ideas 🔮:
- Spotify doesn't notify you when you get a new follower. Maybe something that emails you or notifies you the next time you open spotify if your follower count has changed.
- Ever wonder who's not following you back? A script that tells you who's not following you back on spotify (unfortunately their api doesn't support this rn)
