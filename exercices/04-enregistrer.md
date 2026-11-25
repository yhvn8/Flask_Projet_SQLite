# 🔵 Exercice 4 — Enregistrer un client

⏱️ ~25 minutes · [⬅️ Exercice précédent](03-rechercher.md) · [Exercice suivant ➡️](05-modifier-supprimer.md)

## 🎯 Ce que vous allez découvrir

Jusqu'ici, vous avez **restitué** des informations. Place maintenant à l'**enregistrement** : un formulaire envoie des données en **POST**, Flask les récupère, et une requête **`INSERT`** les range dans la base.

Le formulaire `/enregistrer_client` existe déjà… mais il a **des défauts**. À vous de jouer les testeurs, puis les réparateurs !

## 🛠️ À faire

### Partie A — Jouer les testeurs

1. Visitez `/enregistrer_client`, enregistrez un client, puis regardez le résultat dans `/consultation/`.
2. Comparez votre client avec les autres. **Trouvez les deux anomalies.**
3. Ouvrez `flask_app.py` et `templates/formulaire.html` : retrouvez dans le code l'origine de chaque anomalie.

### Partie B — Réparer

1. Dans `templates/formulaire.html`, ajoutez un champ pour l'adresse :
   ```html
   <label for="adresse">Adresse :</label>
   <input type="text" id="adresse" name="adresse" required><br><br>
   ```
2. Dans la fonction `enregistrer_client()`, récupérez l'adresse avec `request.form['adresse']`.
3. Corrigez la requête `INSERT` : n'indiquez **plus** la colonne `created`, pour que SQLite utilise la valeur par défaut prévue dans `schema.sql` (la date et l'heure actuelles) :
   ```python
   cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, adresse))
   ```
4. *Commit* et testez.

### Partie C — Ne jamais faire confiance au navigateur

L'attribut `required` empêche d'envoyer un formulaire vide… en théorie.

1. Sur `/enregistrer_client`, ouvrez **F12** → onglet **Éléments**, cliquez sur le champ *Nom* et supprimez l'attribut `required` (double-clic dessus). Envoyez le formulaire avec un nom vide.
2. Que contient maintenant votre base ? Un client sans nom !
3. Ajoutez une **validation côté serveur** au début de `enregistrer_client()` :
   ```python
   nom = request.form.get('nom', '').strip().upper()
   prenom = request.form.get('prenom', '').strip()
   adresse = request.form.get('adresse', '').strip()

   if not nom or not prenom or not adresse:
       return render_template('formulaire.html', erreur="Tous les champs sont obligatoires."), 400
   ```
4. Affichez le message d'erreur dans `formulaire.html`, juste sous le titre :
   ```html
   {% if erreur %}
       <p style="color: red;">{{ erreur }}</p>
   {% endif %}
   ```

### Partie D — Le rôle de `commit()`

1. Mettez temporairement la ligne `conn.commit()` en commentaire (ajoutez `#` devant), *commit* sur GitHub, et enregistrez un client.
2. Le client apparaît-il dans `/consultation/` ?
3. Remettez la ligne `conn.commit()` et *commit*.

## 👀 À observer

- Dans **F12 → Réseau**, envoyez le formulaire : cliquez sur la requête `enregistrer_client`. Quelle est sa méthode ? Son code de statut ? Que contient l'onglet **Charge utile** (*Payload*) ?
- Après l'envoi, le navigateur affiche `/consultation/`. Combien de requêtes ont été faites ? Repérez le code `302` : c'est une **redirection**.
- Grâce à `.upper()`, quel que soit ce que tape l'utilisateur, le nom est rangé en majuscules. Pourquoi est-ce utile pour les recherches de l'exercice 3 ?

## 📝 Questions (à noter dans `CARNET.md`)

1. Quelles étaient les deux anomalies du formulaire d'origine, et d'où venaient-elles ?
2. Pourquoi la validation côté **navigateur** (`required`) ne suffit-elle pas ? Pourquoi la garder quand même ?
3. À quoi sert `conn.commit()` ? Que se passe-t-il sans lui ?
4. Pourquoi redirige-t-on vers `/consultation/` après l'enregistrement, au lieu d'afficher directement une page ? (Indice : essayez d'appuyer sur F5 après l'envoi.)

## 🧩 Défi

Après l'enregistrement, redirigez l'utilisateur vers **la fiche du client qu'il vient de créer** plutôt que vers la liste complète. Indice : juste après l'`INSERT`, `cursor.lastrowid` contient l'`id` attribué par SQLite.
