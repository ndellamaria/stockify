from flask import Flask, render_template, request
app = Flask(__name__)

# Homepage
@app.route('/')
def hello_world():
    return 'Hello, World!'

# About
@app.route('/about', methods=['GET','POST'])
def about():
	if request.method == 'POST':
		return render_template('about.html', name=request.form['name'], age=request.form['age'])
	else:
		return render_template('about.html')

app.run()
