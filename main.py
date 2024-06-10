import requests
import urllib.parse
from flask import Flask, redirect, request, jsonify, session, render_template
from datetime import datetime, timedelta
from tqdm import tqdm
import time
import serial
from dotenv import load_dotenv
import os
from unidecode import unidecode

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

def arduino_send(ardu_string):
    arduino.write(bytes(str(ardu_string), 'utf-8'))

def ms_to_time(time):

    millis = time
    seconds=(millis/1000)%60
    seconds = int(seconds)
    minutes=(millis/(1000*60))%60
    minutes = int(minutes)
    hours=(millis/(1000*60*60))%24
    if (hours >= 1):
        return "%0d:%02d:%02d" % (hours, minutes, seconds)

    return "%02d:%02d" % (minutes, seconds)

@app.route('/')
def index():
    return "<a href='/connect_to_arduino'> LOGIN </a>"
    #return "<a href='/login'> LOGIN </a>"

@app.route('/login')
def login():
    scope = "user-read-currently-playing user-read-playback-state user-read-private user-read-email"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": False
    }
    authentication_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(authentication_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post('https://accounts.spotify.com/api/token', data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/current-track')

@app.route('/current-track')
def current_track():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
    "Authorization": f"Bearer {session['access_token']}"
    }

    params = {
        "market": "PL"
    }

    response = requests.get(API_BASE_URL + 'me/player',params=params,headers=headers)
    results = response.json()
    is_playing = results["is_playing"]
    result_name = results["item"]["name"]
    result_artist = results["item"]["artists"][0]["name"]
    track_progress = results["progress_ms"]
    track_duration = results["item"]["duration_ms"]
    track_full = result_artist + " : " + result_name
    timestamp = str(" " + ms_to_time(track_progress) + " | " + ms_to_time(track_duration))
    if (len(timestamp)>16):
        timestamp_shown = str(ms_to_time(track_progress) + " |" + ms_to_time(track_duration))
        #print(timestamp_shown)
    else:
        timestamp_shown = timestamp
        #print(timestamp)
    arduino_string = unidecode(track_full+"~"+timestamp_shown+"~"+str(is_playing))
    #pbar = tqdm(ascii=' ▏▎▍▌▋▊▉█',ncols=16,total=1,bar_format="{desc}: {percentage:3.0f}%[{bar}]")
    #bar = pbar.update(track_percentage)
    #pbar.close()
    
    arduino_send(arduino_string)
    time.sleep(0.1)
    return render_template('index.html', track_full =track_full, timestamp =timestamp_shown, pbar = arduino_string, isPaused=is_playing)

@app.route('/disconnect')
def disconnect():
    serial.Serial.close()
    time.sleep(1)
    return redirect('/')

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/current-track')

@app.route('/connect_to_arduino')
def connect_to_arduino():
    global arduino
    port = input("Please input Arduino COM port number: ")
    arduino = serial.Serial(port='COM'+port, baudrate=115200, timeout=.1)
    time.sleep(3)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
