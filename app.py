from flask import Flask, render_template, request, flash, redirect
from forms import StockForm
from apikeys import client_id, client_secret
from flask_bootstrap import Bootstrap
import requests
import spotipy
import random
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'some_string'

stockList = [
    {
    "name": 'TSLA',
    "quantity": 1,
    "current_price": 10,
    "opening_price": 8,
    "change": 4,
    },
    {
    "name": 'ACB',
    "quantity": 2,
    "current_price": 5,
    "opening_price": 7,
    "change": -8
    }
]

colors = []
for a in stockList:
    if a['change'] >= 0:
        a['change'] = '+' + str(a['change'])
        a['color'] = "w3-text-green"
    else:
        a['color'] = "w3-text-red"

searchq = "sad country"

# form = StockForm()

# Homepage
@app.route('/music')
def hello_world():
    return render_template('music.html')

# About
#@app.route('/about', methods=['GET','POST'])
#def about():
#	if request.method == 'POST':
#		return render_template('about.html', name=request.form['name'], age=request.form['age'])
#	else:
#		return render_template('about.html')

# Table
@app.route('/table', methods=['GET','POST'])
def table():
    form = StockForm()
    if form.validate_on_submit():
        flash('Bought {} stocks of {}.'.format(form.quantity.data,form.ticker.data))
        return redirect('/table')

    # Import from db - just to show functionality

    if request.method == 'POST':
        return render_template('table.html', stockList=stockList, form=form)
    else:
        return render_template('table.html', stockList=stockList, form=form)

@app.route('/generate_playlist',methods=['GET','POST'])
def generate_playlist():

    form = StockForm()

    try:
        access_token = 'dfhsjkdfhds'
        sp = spotipy.Spotify(auth=access_token)
        happytracks = sp.search(q=searchq, limit=30, type='playlist')
    except:

        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}

        url='https://accounts.spotify.com/api/token'

        r=requests.post(url, data=body_params, auth = (client_id, client_secret))
        data = r.json()
        access_token = data['access_token']

        sp = spotipy.Spotify(auth=access_token)

        happytracks = sp.search(q=searchq, limit=20, type='playlist')

    list = happytracks['playlists']['items']

    length = len(list)

    track_names = []
    track_urls = []
    track_images = []
    for track in list:
        track_names.append(track['name'])
        track_urls.append(track['external_urls']['spotify'])
        track_images.append(track['images'][0]['url'])

    n = random.randint(0,length-1)
    one_track_name = track_names[n]
    one_track_url = track_urls[n]
    one_track_image = track_images[n]

    # return render_template('music.html',track_names=track_names,track_urls=track_urls,length=length)

    return render_template('music.html',one_track_url=one_track_url,one_track_name=one_track_name,one_track_image=one_track_image)

app.run()
