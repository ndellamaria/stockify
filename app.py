from flask import Flask, render_template, request, flash, redirect
from forms import StockForm
app = Flask(__name__)

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



app.run()
