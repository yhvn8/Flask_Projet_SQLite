# 🔵 Exercice 5 — Modifier et supprimer

⏱️ ~30 minutes · [⬅️ Exercice précédent](04-enregistrer.md) · [Exercice suivant ➡️](06-faire-evoluer-la-base.md)

## 🎯 Ce que vous allez découvrir

Une application de gestion sait faire quatre opérations de base sur ses données. On les appelle le **CRUD** :

| Opération | Signification | SQL | Où l'avez-vous vu ? |
|---|---|---|---|
| **C**reate | Créer | `INSERT` | Exercice 4 |
| **R**ead | Lire | `SELECT` | Exercices 1 à 3 |
| **U**pdate | Modifier | `UPDATE` | Cet exercice |
| **D**elete | Supprimer | `DELETE` | Cet exercice |

À la fin de cet exercice, votre application de gestion de clients sera **complète** !

## 🛠️ À faire

### Partie A — Supprimer un client

1. Ajoutez cette route dans `flask_app.py` :
   ```python
   @app.route('/supprimer_client/<int:id>', methods=['POST'])
   def supprimer_client(id):
       conn = get_db()
       cursor = conn.cursor()
       cursor.execute('DELETE FROM clients WHERE id = ?', (id,))
       conn.commit()
       conn.close()
       return redirect('/consultation/')
   ```
2. Dans `templates/read_data.html`, ajoutez une colonne *Actions* au tableau, avec un bouton de suppression pour chaque ligne :
   ```html
   <td>
       <form action="/supprimer_client/{{ row['id'] }}" method="post"
             onsubmit="return confirm('Supprimer ce client ?');">
           <button type="submit">🗑️ Supprimer</button>
       </form>
   </td>
   ```
   (N'oubliez pas d'ajouter aussi `<th>Actions</th>` dans la ligne d'en-tête.)
3. *Commit*, puis supprimez un client.

### Partie B — Modifier un client

La modification se fait en deux temps : **afficher** un formulaire pré-rempli (GET), puis **enregistrer** les changements (POST).

1. Créez le template `templates/modifier_client.html` :
   ```html
   <!DOCTYPE html>
   <html lang="fr">
   <head>
       <meta charset="UTF-8">
       <title>Modifier un client</title>
   </head>
   <body>
       <h1>Modifier le client n°{{ client['id'] }}</h1>
       <form method="post">
           <label>Nom : <input type="text" name="nom" value="{{ client['nom'] }}" required></label><br><br>
           <label>Prénom : <input type="text" name="prenom" value="{{ client['prenom'] }}" required></label><br><br>
           <label>Adresse : <input type="text" name="adresse" value="{{ client['adresse'] }}" required></label><br><br>
           <button type="submit">Enregistrer les modifications</button>
       </form>
       <p><a href="/consultation/">Annuler</a></p>
   </body>
   </html>
   ```
2. Ajoutez la route :
   ```python
   @app.route('/modifier_client/<int:id>', methods=['GET', 'POST'])
   def modifier_client(id):
       conn = get_db()
       cursor = conn.cursor()

       if request.method == 'POST':
           cursor.execute('UPDATE clients SET nom = ?, prenom = ?, adresse = ? WHERE id = ?',
                          (request.form['nom'].strip().upper(),
                           request.form['prenom'].strip(),
                           request.form['adresse'].strip(),
                           id))
           conn.commit()
           conn.close()
           return redirect('/consultation/')

       cursor.execute('SELECT * FROM clients WHERE id = ?', (id,))
       client = cursor.fetchone()
       conn.close()
       if client is None:
           return "<h2>Client introuvable</h2>", 404
       return render_template('modifier_client.html', client=client)
   ```
3. Dans `read_data.html`, ajoutez dans la colonne *Actions* un lien vers `/modifier_client/{{ row['id'] }}`.
4. *Commit* et modifiez l'adresse d'un client.

### Partie C — ⚠️ Le `WHERE` oublié

Dans la console **Bash** de PythonAnywhere, ouvrez la base (`cd ~/mysite` puis `sqlite3 database.db`) et observez ce que ferait une requête **sans `WHERE`**… sans casser vos données ! Pour cela, on utilise une **transaction** que l'on annule :
```sql
BEGIN;
UPDATE clients SET nom = 'OUPS';
SELECT id, nom, prenom FROM clients;
ROLLBACK;
SELECT id, nom, prenom FROM clients;
```

## 👀 À observer

- Après le `UPDATE` sans `WHERE`, combien de clients s'appellent `OUPS` ? Et après le `ROLLBACK` ?
- Supprimez le client n°1, puis créez un nouveau client. Quel `id` reçoit-il ? SQLite réutilise-t-il le numéro 1 ? (Regardez le mot-clé `AUTOINCREMENT` dans `schema.sql`.)
- Pourquoi le bouton de suppression est-il un **formulaire POST** et pas un simple lien `<a href="/supprimer_client/3">` ?

## 📝 Questions (à noter dans `CARNET.md`)

1. Que signifie CRUD ? Donnez la requête SQL correspondant à chaque lettre.
2. Que se passe-t-il si l'on oublie le `WHERE` dans un `UPDATE` ou un `DELETE` ? À quoi servent `BEGIN` et `ROLLBACK` ?
3. Pourquoi ne faut-il **jamais** supprimer des données avec une requête GET (un simple lien) ? (Indice : les moteurs de recherche et certains navigateurs « visitent » les liens à l'avance.)
4. Une fois un `id` supprimé, pourquoi est-il préférable qu'il ne soit jamais réattribué à un autre client ?

## 🧩 Défi

Plutôt que de supprimer définitivement un client, de nombreuses applications font une **suppression logique** : on ajoute une colonne `actif` (1 ou 0), et « supprimer » revient à passer `actif` à 0. Les listes n'affichent alors que les clients actifs. Quels sont les avantages de cette méthode ? (Vous saurez ajouter une colonne à l'exercice suivant !)
