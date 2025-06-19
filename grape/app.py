import os

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

from grape import config
from models.wine_model import Wine
from database.db import init_db

app = Flask(__name__)
app.secret_key = config.APP_SECRET  # nécessaire pour utiliser flash
init_db()


@app.route('/')
def index():
    name_filter = request.args.get("name", "")
    min_quantity = request.args.get("min_quantity", "")
    year_filter = request.args.get("year", "")

    wines = Wine.get_all_wines_filtered(name_filter, min_quantity, year_filter)
    return render_template("index.html", wines=wines)


@app.route('/add', methods=['GET', 'POST'])
def add_wine():
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        type = request.form['type']
        quantity = request.form['quantity']
        price = request.form['price']
        volume_ml = request.form['volume_ml']
        purchase_location = request.form['purchase_location']
        cellar_slot = request.form['cellar_slot']
        wine = Wine(name, int(year), type, int(quantity), int(price), int(volume_ml), purchase_location, cellar_slot)
        Wine.add_wine(wine)
        return redirect(url_for('index'))
    return render_template('add_wine.html')

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

@app.route('/wine/<int:wine_id>/consume', methods=['POST'])
def consume_wine(wine_id):
    try:
        to_consume = int(request.form['consumed'])
        wine = Wine.get_wine_by_id(wine_id)

        if wine and to_consume > 0:
            if to_consume > wine.quantity:
                flash(f"Cannot consume {to_consume} bottles. Only {wine.quantity} available.", "danger")
            else:
                wine.quantity -= to_consume
                wine.save()
                flash(f"{to_consume} bouteille(s) consommées", "success")
    except ValueError:
        flash("Invalid input for quantity.", "danger")

    return redirect(url_for('wine_detail', wine_id=wine_id))

@app.route('/wine/<int:wine_id>/update', methods=['POST'])
def update_wine(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if wine:
        wine.name = request.form['name']
        wine.year = request.form['year']
        wine.type = request.form['type']
        wine.quantity = request.form['quantity']
        wine.price = request.form['price']
        wine.cellar_slot = request.form['cellar_slot']
        wine.volume_ml = request.form['volume_ml']
        wine.purchase_location = request.form['purchase_location']
        wine.save()
        flash('Changements sur le vin effectués', 'success')
    return redirect(url_for('wine_detail', wine_id=wine_id))


@app.route('/wine/<int:wine_id>/delete', methods=["GET"])
def delete_wine(wine_id):
    Wine.delete_wine(wine_id)
    flash(f'Le vin est supprimé !', 'success')
    return redirect(url_for('index'))


@app.route('/wine/<int:wine_id>/toggle_favorite', methods=['POST'])
def toggle_favorite(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if wine:
        wine.toggle_favorite()
        flash("Favorite status updated.", "success")
    else:
        flash("Wine not found.", "danger")
    return redirect(url_for('wine_detail', wine_id=wine_id))



if __name__ == '__main__':
    app.run(debug=True)
