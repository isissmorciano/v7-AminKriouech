from app.db import get_db

#Funzioni CRUD per le categorie
def get_all_categories():
	"""Restituisce tutte le categorie ordinate per nome.""" # -> lista categorie ordinate per nome
	db = get_db()
	cur = db.execute("SELECT id, nome FROM categorie ORDER BY nome")
	return cur.fetchall()


def get_category_by_id(category_id):
	"""Restituisce una categoria dato l'id oppure None.""" # -> una singola categoria
	db = get_db()
	cur = db.execute("SELECT id, nome FROM categorie WHERE id = ?", (category_id,))
	return cur.fetchone()


def create_category(nome):
	"""Crea una nuova categoria e restituisce l'id inserito.""" # -> inserisce nuova categoria

	db = get_db()
	cur = db.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
	db.commit()
	return cur.lastrowid
