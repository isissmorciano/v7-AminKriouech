from app.db import get_db

#Funzioni CRUD + Ricerca
def get_all_piatti():
	"""Restituisce tutti i piatti con il nome della categoria. 

	Ordina per nome categoria e poi per nome piatto.
	""" # -> lista di tutti i piatti (con nome categoria)
	db = get_db()
	cur = db.execute(
		"""
		SELECT p.id, p.nome, p.prezzo, p.categoria_id, c.nome AS categoria_nome
		FROM piatti p
		JOIN categorie c ON p.categoria_id = c.id
		ORDER BY c.nome, p.nome
		"""
	)
	return cur.fetchall()


def get_piatti_by_category(category_id):
	"""Restituisce i piatti di una categoria specifica.""" # -> piatti di una categoria specifica
	db = get_db()
	cur = db.execute(
		"""
		SELECT p.id, p.nome, p.prezzo, p.categoria_id, c.nome AS categoria_nome
		FROM piatti p
		JOIN categorie c ON p.categoria_id = c.id
		WHERE p.categoria_id = ?
		ORDER BY p.nome
		""",
		(category_id,),
	)
	return cur.fetchall()


def get_piatto_by_id(piatto_id):
	"""Restituisce un singolo piatto dato l'id.""" # ->  un singolo piatto
	db = get_db()
	cur = db.execute(
		"""
		SELECT p.id, p.nome, p.prezzo, p.categoria_id, c.nome AS categoria_nome
		FROM piatti p
		JOIN categorie c ON p.categoria_id = c.id
		WHERE p.id = ?
		""",
		(piatto_id,),
	)
	return cur.fetchone()


def create_piatto(category_id, nome, prezzo): # -> inserisce nuovo piatto
	"""Inserisce un nuovo piatto e restituisce l'id inserito."""
	db = get_db()
	cur = db.execute(
		"INSERT INTO piatti (categoria_id, nome, prezzo) VALUES (?, ?, ?)",
		(category_id, nome, prezzo),
	)
	db.commit()
	return cur.lastrowid


