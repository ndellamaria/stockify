from flask import Flask, render_template, request, flash, redirect
from forms import StockForm
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'some_string'



# Homepage
@app.route('/')
def hello_world():
    return 'Hello, World!'

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
    stockList = [
        {
        "name": 'TSLA',
        "quantity": 1,
        "current_price": 10,
        "opening_price": 8,
        },
        {
        "name": 'ACB',
        "quantity": 2,
        "current_price": 5,
        "opening_price": 7
        }
    ]


    if request.method == 'POST':
        return render_template('table.html', stockList=stockList, form=form)
    else:
        return render_template('table.html', stockList=stockList, form=form)

@app.route('/generate_playlist',methods=['GET','POST'])
def generate_playlist():

    try:
        sp = spotipy.Spotify(auth=access_token)
    except:
        # client_id
        # client_secret

        grant_type = 'client_credentials'
        body_params = {'grant_type' : grant_type}

        url='https://accounts.spotify.com/api/token'

        r=requests.post(url, data=body_params, auth = (client_id, client_secret))
        data = r.json()
        access_token = data['access_token']

        sp = spotipy.Spotify(auth=access_token)

    happytracks = sp.search(q='happy', limit=20, type='playlist')

    list = happytracks['playlists']['items']

    first = list[0]['name']

    flash('Play some {}.'.format(first))
    # return redirect('/music')
    return render_template('music.html')






app.run()
