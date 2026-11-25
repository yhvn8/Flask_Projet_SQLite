# 🟢 Exercice 1 — Explorer la base en SQL

⏱️ ~20 minutes · [⬅️ Retour au sommaire](../README.md#-séquence-5--les-exercices) · [Exercice suivant ➡️](02-afficher-les-donnees.md)

## 🎯 Ce que vous allez découvrir

Une base de données **relationnelle** range les informations dans des **tables**, comme un tableur :
- une **table** = un type d'objet (ici : les clients) ;
- une **colonne** = une information (le nom, le prénom, l'adresse…) ;
- une **ligne** = un objet précis (le client *Emilie DUPONT*) ;
- la **clé primaire** (`id`) = un numéro unique qui identifie chaque ligne.

Pour parler à la base, on utilise un langage universel : le **SQL** (*Structured Query Language*). Avant de l'utiliser dans Python, vous allez le pratiquer **directement dans la base**.

## 🛠️ À faire

1. Sur PythonAnywhere, ouvrez une console **Bash** (onglet **Consoles**), puis ouvrez votre base :
   ```bash
   cd ~/mysite
   sqlite3 database.db
   ```
   L'invite devient `sqlite>` : vous parlez maintenant directement à la base.
2. Demandez à SQLite de rendre l'affichage lisible (les commandes qui commencent par un point sont propres à SQLite, ce n'est pas du SQL) :
   ```sql
   .headers on
   .mode column
   ```
3. Découvrez la structure de la base :
   ```sql
   .tables
   .schema clients
   ```
   Comparez avec le contenu du fichier `schema.sql` de votre dépôt.
4. Tapez ces requêtes **une par une** (n'oubliez pas le `;` final) et observez le résultat :
   ```sql
   SELECT * FROM clients;
   SELECT nom, prenom FROM clients;
   SELECT nom, prenom FROM clients ORDER BY nom;
   SELECT * FROM clients WHERE id = 3;
   SELECT * FROM clients WHERE adresse LIKE '%Lyon%';
   SELECT COUNT(*) FROM clients;
   ```
5. Ajoutez un client **depuis la console** :
   ```sql
   INSERT INTO clients (nom, prenom, adresse) VALUES ('VOTRE_NOM', 'Votre prénom', '1, rue du Test, 75000 Paris');
   ```
   Puis, **sans rien changer au code**, rechargez la page `/consultation/` de votre site.
6. Quittez la console SQLite avec `.quit`.

> 💡 Un mémo des mots-clés SQL : `SELECT` (choisir les colonnes) · `FROM` (dans quelle table) · `WHERE` (filtrer les lignes) · `ORDER BY` (trier) · `LIMIT` (limiter le nombre de lignes) · `COUNT(*)` (compter).

## 👀 À observer

- Votre nouveau client apparaît sur le site, alors que vous n'avez modifié **aucun fichier** dans GitHub. Pourquoi ?
- Quel `id` a reçu votre client ? Vous ne l'avez pas indiqué dans l'`INSERT` : qui l'a choisi ?
- La colonne `created` a été remplie toute seule. Retrouvez dans `schema.sql` le mot-clé responsable.
- Essayez `INSERT INTO clients (nom) VALUES ('TEST');`. Lisez le message d'erreur.

## 📝 Questions (à noter dans `CARNET.md`)

1. Expliquez avec vos mots la différence entre une **table**, une **colonne** et une **ligne**.
2. À quoi sert la clé primaire `id` ? Pourquoi ne pas simplement identifier un client par son nom ?
3. Pourquoi votre client ajouté en console est-il apparu sur le site ?
4. Que signifie `NOT NULL` dans `schema.sql` ? Quelle erreur avez-vous obtenue avec `INSERT INTO clients (nom) VALUES ('TEST');` ?

## 🧩 Défi

Écrivez les requêtes SQL qui affichent :
- les 3 derniers clients enregistrés (indice : `ORDER BY id DESC` et `LIMIT`) ;
- les clients dont le prénom commence par la lettre **A** ;
- le nombre de clients qui habitent à **Paris**.

Notez vos requêtes dans le carnet.
