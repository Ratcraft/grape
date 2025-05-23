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

@app.route('/wine/<int:wine_id>')
def wine_detail(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if not wine:
        return "Wine not found", 404
    return render_template("wine_detail.html", wine=wine)

@app.route('/wine/<int:wine_id>/edit', methods=["POST"])
def edit_wine(wine_id):
    name = request.form['name']
    year = request.form['year']
    type = request.form['type']
    quantity = request.form['quantity']
    Wine.update_wine(wine_id, name, year, type, quantity)
    return redirect(url_for('wine_detail', wine_id=wine_id))

@app.route('/wine/<int:wine_id>/delete', methods=["POST"])
def delete_wine(wine_id):
    Wine.delete_wine(wine_id)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
