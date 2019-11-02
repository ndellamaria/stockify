from flask import Flask, render_template, request
app = Flask(__name__)

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
def about():
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
        return render_template('table.html', stockList=stockList)
    else:
        return render_template('table.html', stockList=stockList)


app.run()
