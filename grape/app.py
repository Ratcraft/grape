from flask import Flask, render_template, request, redirect, url_for, flash
from grape import config
from grape.models.region import Region
from models.wine import Wine
from models.event import Event
from database.db import init_db

app = Flask(__name__)
app.secret_key = config.APP_SECRET
init_db()


@app.route('/')
def index():
    name_filter = request.args.get("name", "")
    min_quantity = request.args.get("min_quantity", "")
    year_filter = request.args.get("year", "")
    region_id_filter = request.args.get("region_id", "")

    wines = Wine.get_all_wines_filtered(name_filter, min_quantity, year_filter, region_id_filter)
    regions = Region.get_all()

    return render_template("index.html", wines=wines, regions=regions)


@app.route('/add', methods=['GET', 'POST'])
def add_wine():
    if request.method == "POST":
        name = request.form.get("name")
        year = request.form.get("year", type=int)
        wine_type = request.form.get("type")
        quantity = request.form.get("quantity", type=int)
        price = request.form.get("price", type=float)
        volume_ml = request.form.get("volume_ml", type=int)
        cellar_slot = request.form.get("cellar_slot")
        purchase_location = request.form.get("purchase_location")
        medals = request.form.get("medals")
        expiration_date = request.form.get("expiration_date") or None
        region_id = request.form.get("region_id", type=int)

        region = Region.get_by_id(region_id) if region_id else None

        wine = Wine(
            name=name,
            year=year,
            wine_type=wine_type,
            quantity=quantity,
            price=price,
            volume_ml=volume_ml,
            cellar_slot=cellar_slot,
            purchase_location=purchase_location,
            is_favorite=False,
            medals=medals,
            expiration_date=expiration_date,
            region=region
        )

        Wine.add_wine(wine)
        flash("Vin ajouté avec succès", "success")
        return redirect(url_for("index"))  # ou autre route de ton choix

    regions = Region.get_all()  # Assure-toi que cette méthode existe
    return render_template("add_wine.html", regions=regions)


@app.route("/wine/<int:wine_id>", methods=['GET'])
def wine_detail(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if not wine:
        flash("Vin introuvable", "danger")
        return redirect(url_for('index'))

    events = Event.get_events_for_wine(wine_id)
    regions = Region.get_all()
    return render_template("wine_detail.html", wine=wine, events=events, regions=regions)


@app.route('/wine/<int:wine_id>', methods=['POST'])
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
        wine.medals = request.form['medals']
        wine.expiration_date = request.form['expiration_date']
        wine.region = Region.get_by_id(request.form['region_id'])

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


@app.route('/wine/<int:wine_id>/add_event', methods=['POST'])
def add_event(wine_id):
    wine = Wine.get_wine_by_id(wine_id)
    if not wine:
        flash("Wine not found", "danger")
        return redirect(url_for('index'))

    try:
        consumed = int(request.form['consumed_bottles'])
        if consumed <= 0 or consumed > wine.quantity:
            flash("Nombre de bouteilles consommées invalide.", "danger")
            return redirect(url_for('wine_detail', wine_id=wine_id))

        event = Event(
            wine_id=wine_id,
            people=request.form.get('people'),
            food=request.form.get('food'),
            notes=request.form.get('notes'),
            consumed_bottles=consumed
        )
        Event.add_event(event)

        wine.quantity -= consumed
        wine.save()

        flash(f"Événement ajouté et {consumed} bouteille(s) retirée(s).", "success")
    except ValueError:
        flash("Erreur dans le formulaire", "danger")

    return redirect(url_for('wine_detail', wine_id=wine_id))



if __name__ == '__main__':
    app.run(debug=True)
