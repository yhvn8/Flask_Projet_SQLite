# 🔴 Exercice 9 — Créer une API

⏱️ ~30 minutes · [⬅️ Exercice précédent](08-controle-acces.md) · [Projet bibliothèque ➡️](10-projet-bibliotheque.md)

## 🎯 Ce que vous allez découvrir

Jusqu'ici, votre application renvoie des **pages HTML**, faites pour des humains. Mais une application mobile, un autre site ou un script ont besoin des **données brutes**, dans un format facile à lire pour une machine : le **JSON**.

Une **API** (*Application Programming Interface*) est un ensemble de routes qui renvoient (et reçoivent) du JSON. Par convention, on les regroupe sous le préfixe `/api/` :

| Méthode | Route | Action | Équivalent SQL |
|---|---|---|---|
| `GET` | `/api/clients` | Lister les clients | `SELECT` |
| `GET` | `/api/clients/3` | Lire le client n°3 | `SELECT ... WHERE id = 3` |
| `POST` | `/api/clients` | Créer un client | `INSERT` |
| `DELETE` | `/api/clients/3` | Supprimer le client n°3 | `DELETE ... WHERE id = 3` |

## 🛠️ À faire

### Partie A — Lire les données en JSON

1. Ajoutez `jsonify` dans la ligne d'import, en haut de `flask_app.py` :
   ```python
   from flask import Flask, render_template, request, redirect, url_for, session, jsonify
   ```
2. Ajoutez ces deux routes :
   ```python
   @app.get('/api/clients')
   def api_liste_clients():
       conn = get_db()
       rows = conn.execute('SELECT * FROM clients ORDER BY nom').fetchall()
       conn.close()
       return jsonify([dict(row) for row in rows])


   @app.get('/api/clients/<int:id>')
   def api_un_client(id):
       conn = get_db()
       row = conn.execute('SELECT * FROM clients WHERE id = ?', (id,)).fetchone()
       conn.close()
       if row is None:
           return jsonify({'erreur': 'Client introuvable'}), 404
       return jsonify(dict(row))
   ```
3. *Commit*, puis visitez `/api/clients` et `/api/clients/2`, puis `/api/clients/999`.

### Partie B — Envoyer des données en JSON

1. Ajoutez la route de création :
   ```python
   @app.post('/api/clients')
   def api_creer_client():
       donnees = request.get_json(silent=True) or {}
       nom = str(donnees.get('nom', '')).strip().upper()
       prenom = str(donnees.get('prenom', '')).strip()
       adresse = str(donnees.get('adresse', '')).strip()

       if not nom or not prenom or not adresse:
           return jsonify({'erreur': 'Les champs nom, prenom et adresse sont obligatoires'}), 400

       conn = get_db()
       cursor = conn.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)',
                             (nom, prenom, adresse))
       conn.commit()
       nouvel_id = cursor.lastrowid
       conn.close()
       return jsonify({'id': nouvel_id, 'nom': nom, 'prenom': prenom, 'adresse': adresse}), 201
   ```
2. Un navigateur ne sait envoyer une requête POST en JSON que via JavaScript. Sur votre site, ouvrez **F12** → onglet **Console**, et tapez :
   ```javascript
   fetch('/api/clients', {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({nom: 'Api', prenom: 'Test', adresse: '1, rue du JSON, 75000 Paris'})
   }).then(r => r.json()).then(console.log)
   ```
3. Vérifiez sur `/api/clients` que le client a bien été créé. Recommencez en oubliant le champ `adresse`.

### Partie C — Protéger l'API

Votre API de création est ouverte à tous ! Appliquez la même règle qu'à l'exercice 8 : seul un `admin` connecté peut créer un client. Pour une API, on ne redirige pas vers un formulaire : on renvoie une **erreur en JSON** :
```python
if not a_le_role('admin'):
    return jsonify({'erreur': 'Authentification administrateur requise'}), 401
```
Testez la commande `fetch` de la partie B **connecté** puis **déconnecté**.

## 👀 À observer

- Dans **F12 → Réseau**, comparez la réponse de `/consultation/` et celle de `/api/clients` : regardez l'en-tête `Content-Type` de chacune.
- Quel code de statut renvoie la création ? Pourquoi `201` plutôt que `200` ?
- Les pages HTML et l'API utilisent **la même base de données**. Un client créé par l'API apparaît-il dans `/consultation/` ?

## 📝 Questions (à noter dans `CARNET.md`)

1. Quelle est la différence entre une page HTML et une réponse JSON ? À qui chacune est-elle destinée ?
2. Que signifient les codes `200`, `201`, `400`, `401` et `404` renvoyés par votre API ?
3. Pourquoi une API renvoie-t-elle une erreur JSON plutôt qu'une redirection vers la page de connexion ?
4. Citez une application de votre téléphone qui, selon vous, utilise une API. Quelles données échange-t-elle ?

## 🧩 Défi

1. Ajoutez la route `DELETE /api/clients/<id>` (réservée aux admins), et testez-la avec `fetch` et `method: 'DELETE'`.
2. Ajoutez un paramètre de recherche : `/api/clients?q=dup` ne renvoie que les clients correspondants (réutilisez le `LIKE` de l'exercice 3).
3. Créez une page HTML qui, en JavaScript, appelle `/api/clients` avec `fetch` et affiche la liste **sans recharger la page**.
