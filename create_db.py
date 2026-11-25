# ---------------------------------------------------------------
#  Création (ou RÉ-initialisation) de la base de données
# ---------------------------------------------------------------
#  ⚠️ Attention : ce script EFFACE toutes les données existantes
#  (voir les "DROP TABLE" dans schema.sql) puis recrée les tables
#  avec quelques données d'exemple.
#
#  À lancer depuis une console Bash PythonAnywhere :
#      cd ~/mysite
#      python3 create_db.py
# ---------------------------------------------------------------

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

connection = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))

with open(os.path.join(BASE_DIR, 'schema.sql'), encoding='utf-8') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'))
cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)", ('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris'))

connection.commit()
connection.close()

print("✅ Base de données créée : database.db")
