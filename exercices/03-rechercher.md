# 🟢 Exercice 3 — Rechercher un client

⏱️ ~30 minutes · [⬅️ Exercice précédent](02-afficher-les-donnees.md) · [Exercice suivant ➡️](04-enregistrer.md)

## 🎯 Ce que vous allez découvrir

Restituer **toutes** les données, c'est facile. Restituer **les bonnes** données, c'est l'essentiel du travail ! Vous allez créer une recherche, et découvrir au passage **la faille de sécurité la plus célèbre du Web : l'injection SQL**.

## 🛠️ À faire

### Partie A — Une route de recherche par nom

Créez une nouvelle route **`/fiche_nom/<nom>`** qui affiche les clients portant ce nom. Inspirez-vous de `Readfiche()` :
```python
@app.route('/fiche_nom/<nom>')
def fiche_nom(nom):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)
```
*Commit*, puis testez `/fiche_nom/DUPONT`, puis `/fiche_nom/dupont`.

> 💡 Le `?` dans la requête est un **paramètre** : SQLite le remplace lui-même par la valeur fournie dans le tuple `(nom,)`. La virgule est obligatoire : sans elle, `(nom)` n'est pas un tuple !

### Partie B — Un formulaire de recherche

Personne ne tape une URL à la main : ajoutons un vrai champ de recherche.

1. Créez le template `templates/recherche.html` :
   ```html
   <!DOCTYPE html>
   <html lang="fr">
   <head>
       <meta charset="UTF-8">
       <title>Recherche</title>
   </head>
   <body>
       <h1>Rechercher un client</h1>
       <form action="/recherche" method="get">
           <input type="text" name="q" value="{{ q }}" placeholder="Nom ou prénom...">
           <button type="submit">Rechercher</button>
       </form>

       {% if q %}
           <p>{{ data|length }} résultat(s) pour « {{ q }} »</p>
           <ul>
           {% for row in data %}
               <li><a href="/fiche_client/{{ row['id'] }}">{{ row['nom'] }} {{ row['prenom'] }}</a></li>
           {% endfor %}
           </ul>
       {% endif %}
   </body>
   </html>
   ```
2. Ajoutez la route dans `flask_app.py` :
   ```python
   @app.route('/recherche')
   def recherche():
       q = request.args.get('q', '').strip()
       data = []
       if q:
           conn = get_db()
           cursor = conn.cursor()
           motif = '%' + q + '%'
           cursor.execute('SELECT * FROM clients WHERE nom LIKE ? OR prenom LIKE ? ORDER BY nom',
                          (motif, motif))
           data = cursor.fetchall()
           conn.close()
       return render_template('recherche.html', q=q, data=data)
   ```
3. *Commit*, visitez `/recherche` et cherchez `ma`, puis `LU`. Regardez la barre d'adresse après la recherche.

### Partie C — ⚠️ L'injection SQL (à ne jamais reproduire en vrai !)

Un développeur pressé aurait pu écrire la requête de la partie A **en collant directement** le texte de l'utilisateur dans le SQL. Ajoutez temporairement cette route :
```python
@app.route('/fiche_nom_dangereuse/<nom>')
def fiche_nom_dangereuse(nom):
    conn = get_db()
    cursor = conn.cursor()
    requete = "SELECT * FROM clients WHERE nom = '" + nom + "'"  # ❌ NE FAITES JAMAIS ÇA
    print(requete, flush=True)  # la requête réellement exécutée apparaîtra dans le Server log
    cursor.execute(requete)
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)
```
1. Testez `/fiche_nom_dangereuse/DUPONT` : tout semble fonctionner.
2. Testez maintenant `/fiche_nom_dangereuse/x' OR '1'='1` …
3. Allez lire le **Server log** sur PythonAnywhere (onglet **Web**) pour voir la requête réellement exécutée.
4. Testez la même chose sur la route sûre : `/fiche_nom/x' OR '1'='1`.
5. **Supprimez la route dangereuse** de votre code, puis *commit*.

## 👀 À observer

- `/fiche_nom/dupont` ne trouve rien, alors que la recherche `/recherche?q=dupont` fonctionne. Quelle est la différence entre `=` et `LIKE` ?
- Avec la route dangereuse, combien de clients s'affichent ? Pourquoi ?
- Dans la recherche, tapez `<b>test</b>` : le texte s'affiche-t-il en gras dans « résultat(s) pour… » ? Faites un clic droit → **Afficher le code source**. Flask a protégé votre page !

## 📝 Questions (à noter dans `CARNET.md`)

1. Quelle est la différence entre `WHERE nom = 'DUPONT'` et `WHERE nom LIKE '%DUP%'` ?
2. Expliquez avec vos mots ce qu'est une **injection SQL**. Qu'est-ce qu'un pirate pourrait faire de pire qu'afficher tous les clients ?
3. Pourquoi la version avec `?` est-elle protégée contre l'injection ?
4. Pour la recherche, on a utilisé `method="get"`. Quel avantage pour l'utilisateur ? (Indice : favoris, partage de lien.)

## 🧩 Défi

Ajoutez au formulaire de recherche une liste déroulante pour choisir le **critère de tri** (par nom, par prénom, par date de création).

⚠️ Attention : on **ne peut pas** utiliser `?` pour un nom de colonne dans `ORDER BY`. Comment faire, sans ouvrir de faille d'injection ? (Indice : une liste des valeurs autorisées en Python.)
