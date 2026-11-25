# 🟣 Exercice 6 — Faire évoluer la base

⏱️ ~20 minutes · [⬅️ Exercice précédent](05-modifier-supprimer.md) · [Exercice suivant ➡️](07-relier-deux-tables.md)

## 🎯 Ce que vous allez découvrir

Votre client vous demande d'enregistrer **le numéro de téléphone** de ses clients. Il faut donc ajouter une **colonne** à la table. Facile ? Oui… à condition de **ne pas perdre les données déjà enregistrées** !

Vous allez découvrir qu'une base de données a deux facettes :
- sa **structure** (le *schéma* : les tables et les colonnes), décrite dans `schema.sql` ;
- son **contenu** (les données), qui vit uniquement dans `database.db`, sur le serveur.

## 🛠️ À faire

### Partie A — Comprendre le piège

Ouvrez `schema.sql` et `create_db.py`. Répondez (dans votre tête) :
- Que fait la première ligne de `schema.sql` (`DROP TABLE IF EXISTS clients;`) ?
- Si vous ajoutez la colonne dans `schema.sql`, puis relancez `create_db.py` sur le serveur, que deviennent les clients que vous avez saisis aux exercices 4 et 5 ?

👉 Relancer `create_db.py`, c'est pratique pendant le développement… mais **catastrophique en production**, quand de vrais utilisateurs ont saisi des données.

### Partie B — Ajouter la colonne sans rien perdre

1. Dans la console **Bash** de PythonAnywhere :
   ```bash
   cd ~/mysite
   sqlite3 database.db
   ```
2. Ajoutez la colonne avec `ALTER TABLE`, puis vérifiez :
   ```sql
   ALTER TABLE clients ADD COLUMN telephone TEXT;
   .schema clients
   .headers on
   .mode column
   SELECT * FROM clients;
   .quit
   ```
   Vos clients sont toujours là ; leur téléphone est vide (`NULL`).
3. **Mettez aussi à jour `schema.sql`** sur GitHub, pour que la structure du code et celle de la base restent identiques (utile si vous, ou un collègue, recréez la base un jour) :
   ```sql
   CREATE TABLE clients (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       nom TEXT NOT NULL,
       prenom TEXT NOT NULL,
       adresse TEXT NOT NULL,
       telephone TEXT
   );
   ```

### Partie C — Utiliser la nouvelle colonne

Faites le travail **sur toute la chaîne** :
1. **Formulaire** (`formulaire.html`) : ajoutez un champ `telephone` (non obligatoire).
2. **Enregistrement** (`enregistrer_client()`) : ajoutez la colonne et la valeur dans l'`INSERT`.
3. **Affichage** (`read_data.html`) : ajoutez une colonne *Téléphone* au tableau.
4. **Modification** (`modifier_client.html` et `modifier_client()`) : permettez de modifier le téléphone.

## 👀 À observer

- Pourquoi le robot de déploiement (fichier `.github/workflows/deploy-pythonanywhere.yml`) ignore-t-il les fichiers `*.db` ? Cherchez la ligne correspondante et lisez le commentaire.
- Pourquoi le fichier `.gitignore` contient-il `*.db` ?
- Pour les clients créés avant l'ajout de la colonne, que s'affiche-t-il dans le tableau ? Comment afficher un tiret `-` à la place ? (Indice : `{{ row['telephone'] or '-' }}`)

## 📝 Questions (à noter dans `CARNET.md`)

1. Quelle est la différence entre le **schéma** d'une base et ses **données** ? Où se trouve chacun ?
2. Pourquoi ne faut-il pas relancer `create_db.py` sur une application en production ?
3. Pourquoi est-il important de garder `schema.sql` à jour, même si on a modifié la base avec `ALTER TABLE` ?
4. Pour ajouter **une** information, combien de fichiers avez-vous dû modifier ? Lesquels ?

## 🧩 Défi

En entreprise, chaque modification de la structure est rangée dans un petit script numéroté (`migrations/001_ajout_telephone.sql`, `002_...`), que l'on exécute une seule fois sur chaque serveur. Créez le dossier `migrations/` et votre première migration. Quel est l'intérêt de garder cet historique ?
