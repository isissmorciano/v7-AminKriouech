from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.repositories import categoria_repository, piatto_repository

bp = Blueprint("main", __name__)


@bp.route("/") # -> lista categorie (index)
def index():
	"""Lista categorie (home)."""
	categorie = categoria_repository.get_all_categories()
	return render_template("index.html", categorie=categorie)


@bp.route("/categoria/<int:category_id>") # -> dettaglio categoria con lista piatti
def categoria_detail(category_id):
	"""Dettaglio categoria con lista piatti."""
	categoria = categoria_repository.get_category_by_id(category_id)
	if categoria is None:
		abort(404)
	piatti = piatto_repository.get_piatti_by_category(category_id)
	return render_template("categoria_detail.html", categoria=categoria, piatti=piatti)


@bp.route("/crea_categoria", methods=("GET", "POST")) # -> salva categoria nel DB
def crea_categoria():
	if request.method == "POST":
		nome = request.form.get("nome", "").strip()
		if not nome:
			flash("Il nome della categoria è obbligatorio.")
			return render_template("crea_categoria.html", nome=nome)

		categoria_repository.create_category(nome)
		flash("Categoria creata con successo.")
		return redirect(url_for("main.index"))

	return render_template("crea_categoria.html")


@bp.route("/crea_piatto", methods=("GET", "POST")) # -> salva categoria nel DB
def crea_piatto():
	categorie = categoria_repository.get_all_categories()

	if request.method == "POST":
		nome = request.form.get("nome", "").strip()
		prezzo_raw = request.form.get("prezzo", "").strip()
		categoria_id = request.form.get("categoria_id")

		# Validazione
		error = None
		if not nome:
			error = "Il nome del piatto è obbligatorio."
		elif not prezzo_raw:
			error = "Il prezzo è obbligatorio."
		elif not categoria_id:
			error = "Seleziona una categoria."

		try:
			prezzo = float(prezzo_raw)
			if prezzo <= 0:
				error = "Il prezzo deve essere un numero positivo."
		except ValueError:
			prezzo = None
			if prezzo_raw:
				error = "Prezzo non valido."

		# Controlla categoria esistente
		if categoria_id:
			cat = categoria_repository.get_category_by_id(categoria_id)
			if cat is None:
				error = "Categoria selezionata non esistente."

		if error:
			flash(error)
			return render_template("crea_piatto.html", categorie=categorie, nome=nome, prezzo=prezzo_raw, categoria_id=categoria_id)

		# Inserisci piatto
		piatto_repository.create_piatto(categoria_id, nome, prezzo)
		flash("Piatto creato con successo.")
		return redirect(url_for("main.categoria_detail", category_id=categoria_id))

	return render_template("crea_piatto.html", categorie=categorie)

# Route per la ricerca
@bp.route("/ricerca", methods=("GET", "POST"))
def ricerca():
	results = None
	term = ""
	if request.method == "POST":
		term = request.form.get("term", "").strip()
		if term:
			results = piatto_repository.find_piatti_by_name(term)
		else:
			flash("Inserisci un termine di ricerca.")

	return render_template("ricerca.html", results=results, term=term)


			
