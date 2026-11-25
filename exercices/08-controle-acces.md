# 🔴 Exercice 8 — Contrôle d'accès

⏱️ ~30 minutes · [⬅️ Exercice précédent](07-relier-deux-tables.md) · [Exercice suivant ➡️](09-api-json.md)

## 🎯 Ce que vous allez découvrir

Pour l'instant, **n'importe quel internaute** peut supprimer vos clients ! Une vraie application distingue :
- l'**authentification** : *qui êtes-vous ?* (identifiant + mot de passe) ;
- l'**autorisation** : *qu'avez-vous le droit de faire ?* (selon votre **rôle**).

| Rôle | Identifiants | Droits |
|---|---|---|
| Visiteur (non connecté) | – | Page d'accueil uniquement |
| **user** | `user` / `12345` | Consulter et rechercher |
| **admin** | `admin` / `password` | Tout, y compris enregistrer, modifier et supprimer |

Comment le serveur se souvient-il que vous êtes connecté, d'une page à l'autre ? Grâce à la **session**, stockée dans un **cookie** de votre navigateur.

## 🛠️ À faire

### Partie A — Observer la session existante

1. Visitez `/lecture` : vous êtes redirigé vers `/authentification`.
2. Connectez-vous avec `admin` / `password`, puis ouvrez **F12** → onglet **Application** (Chrome/Edge) ou **Stockage** (Firefox) → **Cookies**. Repérez le cookie `session`.
3. Supprimez ce cookie, puis rechargez `/lecture`. Que se passe-t-il ?

### Partie B — Gérer deux rôles

1. Dans `flask_app.py`, remplacez la fonction `authentification()` pour gérer les deux comptes et mémoriser le **rôle** dans la session :
   ```python
   # Comptes de démonstration (à remplacer par une table en base : voir le défi)
   COMPTES = {
       'admin': {'mot_de_passe': 'password', 'role': 'admin'},
       'user': {'mot_de_passe': '12345', 'role': 'user'},
   }

   @app.route('/authentification', methods=['GET', 'POST'])
   def authentification():
       if request.method == 'POST':
           compte = COMPTES.get(request.form['username'])
           if compte and request.form['password'] == compte['mot_de_passe']:
               session['authentifie'] = True
               session['utilisateur'] = request.form['username']
               session['role'] = compte['role']
               return redirect(url_for('lecture'))
           return render_template('formulaire_authentification.html', error=True)

       return render_template('formulaire_authentification.html', error=False)
   ```
2. Ajoutez, sous la fonction `est_authentifie()`, une fonction qui vérifie le rôle :
   ```python
   def a_le_role(*roles):
       """Renvoie True si l'utilisateur connecté a l'un des rôles indiqués."""
       return session.get('role') in roles
   ```
3. Ajoutez une route de déconnexion :
   ```python
   @app.route('/deconnexion')
   def deconnexion():
       session.clear()
       return redirect('/')
   ```

### Partie C — Protéger les routes

1. Protégez la route de recherche **`/fiche_nom/<nom>`** (exercice 3) : seuls les rôles `user` et `admin` y ont accès. Ajoutez au début de la fonction :
   ```python
   if not a_le_role('user', 'admin'):
       return redirect(url_for('authentification'))
   ```
2. Protégez de la même façon `/consultation/`, `/fiche_client/<id>` et `/recherche`.
3. Protégez les routes d'**écriture** (`/enregistrer_client` en GET **et** en POST, `/modifier_client`, `/supprimer_client`) : seul `admin` y a accès. Si un `user` connecté essaie, renvoyez le code **403** (*Forbidden*) :
   ```python
   if not a_le_role('admin'):
       return "<h2>Accès refusé : réservé aux administrateurs</h2>", 403
   ```
4. Dans `read_data.html`, n'affichez les boutons *Modifier* et *Supprimer* qu'aux administrateurs :
   ```html
   {% if session['role'] == 'admin' %}
       ... vos boutons ...
   {% endif %}
   ```
5. *Commit*, puis testez **méthodiquement** chaque route avec : aucun compte, `user`, puis `admin`.

## 👀 À observer

- Connecté en `user`, les boutons *Supprimer* ont disparu. Mais si vous envoyez quand même la requête (par exemple en recréant le bouton dans l'onglet **Éléments** de F12) ? Le serveur vous bloque-t-il ?
- Copiez la valeur du cookie `session` **jusqu'au premier point** (`.`) et collez-la sur un site de décodage Base64 : vous pouvez lire votre rôle ! Le cookie est **signé**, pas **chiffré**. Pourquoi ne peut-on pas, pour autant, le modifier pour devenir admin ? (Indice : `app.secret_key`.)

## 📝 Questions (à noter dans `CARNET.md`)

1. Quelle est la différence entre **authentification** et **autorisation** ?
2. Où est stockée la session ? Comment le serveur sait-il qui vous êtes à chaque nouvelle requête ?
3. Pourquoi masquer un bouton dans le HTML ne suffit-il pas à protéger une action ?
4. Que signifient les codes `302` et `403` ? Dans quel cas votre application renvoie-t-elle chacun d'eux ?
5. Le mot de passe `password` est écrit en clair dans `flask_app.py`, sur un dépôt **public**. Quel est le risque ? Quelle solution avez-vous déjà rencontrée dans cet atelier pour cacher une information sensible ?

## 🧩 Défi (indispensable pour la séquence 6 !)

Rangez les comptes **dans la base de données** plutôt que dans le code :
1. Créez une table `utilisateurs (id, login, mot_de_passe_hash, role)`.
2. Ne stockez **jamais** un mot de passe en clair : utilisez les fonctions de hachage fournies avec Flask :
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash

   generate_password_hash('12345')   # → 'scrypt:32768:8:1$...' : à stocker en base
   check_password_hash(hash_en_base, mot_de_passe_saisi)   # → True ou False
   ```
3. Modifiez `authentification()` pour vérifier le login et le mot de passe à partir de cette table.

Pourquoi stocker un *hash* plutôt que le mot de passe ? Que se passerait-il si la base était volée ?
