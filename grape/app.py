from flask import Flask, render_template, request, redirect, url_for, flash
from grape import config
from models.wine_model import Wine
from database.db import init_db

app = Flask(__name__)
app.secret_key = config.APP_SECRET
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
        try:
            wine = Wine(
                name=request.form['name'],
                year=int(request.form['year']),
                type=request.form['type'],
                quantity=int(request.form['quantity']),
                price=float(request.form['price']),
                volume_ml=int(request.form['volume_ml']),
                purchase_location=request.form['purchase_location'],
                cellar_slot=request.form['cellar_slot'],
                is_favorite=False
            )
            Wine.add_wine(wine)
            flash("Vin ajouté avec succès.", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Erreur lors de l'ajout : {e}", "danger")
    return render_template('add_wine.html')


@app.route('/wine/<int:wine_id>')
def wine_detail(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if not wine:
        flash("Vin non trouvé.", "danger")
        return redirect(url_for('index'))
    return render_template("wine_detail.html", wine=wine)


@app.route('/wine/<int:wine_id>/edit', methods=['POST'])
def edit_wine(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if wine:
        wine.name = request.form['name']
        wine.year = int(request.form['year'])
        wine.type = request.form['type']
        wine.quantity = int(request.form['quantity'])
        wine.price = float(request.form['price'])
        wine.volume_ml = int(request.form['volume_ml'])
        wine.purchase_location = request.form['purchase_location']
        wine.cellar_slot = request.form['cellar_slot']
        wine.save()
        flash("Modifications enregistrées.", "success")
    else:
        flash("Vin non trouvé.", "danger")
    return redirect(url_for('wine_detail', wine_id=wine_id))


@app.route('/wine/<int:wine_id>/delete')
def delete_wine(wine_id):
    if Wine.delete_wine(wine_id):
        flash("Vin supprimé.", "success")
    else:
        flash("Vin introuvable.", "danger")
    return redirect(url_for('index'))


@app.route('/wine/<int:wine_id>/consume', methods=['POST'])
def consume_wine(wine_id):
    try:
        to_consume = int(request.form['consumed'])
        wine = Wine.get_wine_by_id(wine_id)
        if wine and to_consume > 0:
            if to_consume > wine.quantity:
                flash(f"Impossible de consommer {to_consume} bouteilles. Seulement {wine.quantity} disponible(s).", "danger")
            else:
                wine.quantity -= to_consume
                wine.save()
                flash(f"{to_consume} bouteille(s) consommée(s).", "success")
        else:
            flash("Quantité invalide.", "danger")
    except ValueError:
        flash("Entrée invalide.", "danger")

    return redirect(url_for('wine_detail', wine_id=wine_id))


@app.route('/wine/<int:wine_id>/toggle_favorite', methods=['POST'])
def toggle_favorite(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if wine:
        wine.toggle_favorite()
        wine.save()
        flash("Statut favori mis à jour.", "success")
    else:
        flash("Vin non trouvé.", "danger")
    return redirect(url_for('wine_detail', wine_id=wine_id))


@app.route('/info')
def wine_info():
    return render_template('wine_info.html')


if __name__ == '__main__':
    app.run(debug=True)
