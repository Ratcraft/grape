from flask import Flask, render_template, request, redirect, url_for
from models.wine_model import Wine
from database.db import init_db

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    wines = Wine.get_all_wines()
    return render_template('index.html', wines=wines)

@app.route('/add', methods=['POST'])
def add_wine():
    name = request.form['name']
    year = request.form['year']
    type = request.form['type']
    quantity = request.form['quantity']
    wine = Wine(name, int(year), type, int(quantity))
    Wine.add_wine(wine)
    return redirect(url_for('index'))

@app.route('/info')
def wine_info():
    return render_template('wine_info.html')

if __name__ == '__main__':
    app.run(debug=True)
