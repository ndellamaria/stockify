from flask import Flask, render_template, request, flash, redirect
from forms import StockForm, GenreForm
from apikeys import client_id, client_secret, api_token
from flask_bootstrap import Bootstrap
import requests
import spotipy
import random
import collections
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'some_string'

FINAL_CHANGE = [0]
chosen_genre = [0]

f = open('NASDAQ.txt')

tickerSet = set()

for line in f.readlines():
    tickerSet.add(line.split()[0])

# stockList = [
#     {
#     "name": 'TSLA',
#     "quantity": 1,
#     "current_price": 10,
#     "opening_price": 8,
#     "change": 4,
#     },
#     {
#     "name": 'ACB',
#     "quantity": 2,
#     "current_price": 5,
#     "opening_price": 7,
#     "change": -8
#     }
# ]

genres = ['country','pop','alternative','rock','electronic','party','jazz','classical']

# colors = []
# for a in stockList:
#     if a['change'] >= 0:
#         a['change'] = '+' + str(a['change'])
#         a['color'] = "w3-text-green"
#     else:
#         a['color'] = "w3-text-red"

searchq = "classical"

# Table
stocksList = collections.OrderedDict()
# final_change=0
@app.route('/table', methods=['GET','POST'])
def table():
    form1 = StockForm()
    form2 = GenreForm()

    chosen_genre[0] = form2.genre.data

    final_change=0

    msg = ''
    if form1.validate_on_submit():
        ticker = form1.ticker.data
        quantity = form1.quantity.data

        if ticker not in tickerSet:
            msg = 'Please enter a valid ticker.'
            # return render_template('table.html', stocksList=stocksList, msg=msg, form=form, final_change=final_change)
        elif ticker in stocksList:
            stocksList[ticker]['quantity']+=quantity
        else:
            stocksList[ticker] = {'name':ticker}
            stocksList[ticker]['quantity']=quantity
        symbols_list = ''
        for s in list(stocksList.keys()):
            symbols_list+=s+','
        symbols_list=symbols_list[:-1]
        PARAMS = {
            'symbol': symbols_list,
            'api_token': api_token
        }

        response = requests.get('https://api.worldtradingdata.com/api/v1/stock',params=PARAMS)
        data = response.json()


        for stock in data['data']:
            final_change += float(stock['day_change'])*float(stocksList[stock['symbol']]['quantity'])
            FINAL_CHANGE[0] = final_change
            stocksList[stock['symbol']]['current_price'] = stock['price']
            stocksList[stock['symbol']]['opening_price'] = stock['price_open']
            stocksList[stock['symbol']]['change'] = round(float(stock['day_change'])*float(stocksList[stock['symbol']]['quantity']),2)

        for stock in stocksList:
            if stocksList[stock]['change'] >= 0:
                stocksList[stock]['change'] = '+' + str(stocksList[stock]['change'])
                stocksList[stock]['color'] = "w3-text-green"
            else:
                stocksList[stock]['color'] = "w3-text-red"

    if request.method == 'POST':
        return render_template('table.html', stockList=stocksList, form1=form1,form2=form2, genres=genres)
    else:
        return render_template('table.html', stockList=stocksList, form1=form1, form2=form2, genres=genres)

@app.route('/music',methods=['GET','POST'])
def generate_playlist():
    final_change = FINAL_CHANGE[0]
    searchq = chosen_genre[0]

    if final_change >= 0:
        searchq = "happy " + searchq
    elif final_change <= -100:
        searchq = "cry " + searchq
    else:
        searchq = "sad " + searchq

    print(searchq)

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
