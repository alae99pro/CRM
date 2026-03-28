# Documentation : Modèles et Vues du Module Reporting

Ce document détaille la structure backend du module Reporting de **FenyCare CRM**. Pour le MVP, le module `reporting` ne possède pas de modèles complexes qui lui sont propres ; il agit principalement comme un agrégateur de données provenant des autres modules (CRM, Supply Chain, Marketing) via ses vues.

---

## 1. Modèles (`reporting/models.py`)

Actuellement, le fichier `models.py` du module reporting est vide de classes.
**Décision MVP :** Le reporting est basé sur des requêtes directes (`QuerySets` et Agrégations Django) vers les tables existantes. Aucune table de base de données spécifique au reporting (comme des tables de matérialisation de données ou d'entrepôt de données) n'est nécessaire pour le moment.

Les modèles interrogés par le reporting sont :
- **CRM :** `Client`, `Prospect`
- **Supply Chain :** `Commande`, `LigneCommande`, `Produit`
- **Marketing :** `Campagne`, `EmailEnvoye`

---

## 2. Vues (`reporting/views.py`)

Les vues du module reporting sont responsables de la récupération, du filtrage par période, et de l'agrégation des données avant de les envoyer aux templates.

Toutes les vues sont protégées par le décorateur `@login_required`.

### 2.1 `rapport_ventes(request)`
**Objectif :** Analyser les performances commerciales.
- **Filtre principal :** Période dynamique (`periode` passée en GET : 7, 30, 90, 365 jours).
- **Données calculées :**
  - **Statistiques globales (`stats`) :** Nombre total de commandes, Chiffre d'Affaires (CA) total (statut `livree`), Panier moyen, et commandes en cours (hors `livree` et `annulee`).
  - **Série temporelle (`ventes_par_jour`) :** Agrégation par date (`TruncDate`) du CA et du nombre de commandes pour tracer l'évolution temporelle.
  - **Top Produits (`top_produits`) :** Les 10 produits générant le plus de CA sur la période.
  - **Segmentation (`ventes_par_type`) :** Répartition du CA par type de client (ex: B2B, B2C).
- **Template cible :** `reporting/rapport_ventes.html`

### 2.2 `rapport_clients(request)`
**Objectif :** Suivre l'acquisition, la fidélisation et la conversion.
- **Filtre principal :** Période dynamique (jours).
- **Données calculées :**
  - **Statistiques globales (`stats`) :** Total clients, nouveaux clients sur la période, clients actifs, total prospects, prospects actifs (statuts `prospect` ou `en_cours`).
  - **Répartition (`clients_par_type`) :** Nombre de clients agrégé par type (B2B, B2C...).
  - **Top Clients (`top_clients`) :** Les 10 clients ayant généré le plus de CA sur la période.
  - **Entonnoir de Conversion (`prospects_stats` & `taux_conversion`) :** Comptage par statut des prospects (Nouveau, En Cours, Gagné, Perdu) et calcul du `taux_conversion` (Gagné / Total).
- **Template cible :** `reporting/rapport_clients.html`

### 2.3 `rapport_marketing(request)`
**Objectif :** Mesurer les performances des campagnes d'emailing.
- **Filtre principal :** Période dynamique (jours).
- **Données calculées :**
  - **Statistiques globales (`stats`) :** Total campagnes, campagnes actives, total emails envoyés, taux d'ouverture global, taux de clic global.
  - **Top Campagnes (`campagnes_perf`) :** Liste des 10 dernières campagnes ayant effectué des envois.
  - **Série temporelle (`emails_par_jour`) :** Évolution quotidienne du nombre d'emails envoyés et ouverts sur la période (utilisant `TruncDate` et `Count` conditionnel).
- **Template cible :** `reporting/rapport_marketing.html`

### 2.4 `rapport_stock(request)`
**Objectif :** Superviser la valeur et la rotation du stock (vision instantanée + historique récent de vente).
- **Données calculées :**
  - **Statistiques conditionnelles (`stats`) :** Total produits, produits actifs, nombre de produits ayant atteint le seuil de `stock_bas`, et la valeur financière totale du stock actuel.
  - **Alertes (`produits_stock_bas`) :** Liste des 20 premiers produits nécessitant un réapprovisionnement.
  - **Rotation (`produits_vendus`) :** Les 10 produits les plus vendus (en volume) sur les 90 derniers jours, pour comprendre ce qui draine le stock.
- **Template cible :** `reporting/rapport_stock.html`

### 2.5 `export_data(request)`
**Objectif :** Fournir une interface pour télécharger les données brutes.
- **Logique actuelle :** La vue se contente de rendre le template (`reporting/export_data.html`). 
- **Évolution future (MVP / V2) :** Cette vue devra intercepter la méthode GET pour générer un objet `HttpResponse` avec le type de contenu `text/csv` (ou `application/vnd.ms-excel` avec `pandas` / `openpyxl`), itérer sur les modèles ciblés (Commandes, Clients, etc.) et écrire les lignes avec le module natif `csv` de Python avant de retourner le fichier au navigateur.

---

## 3. Directives de Codage (Best Practices)

Pour assurer la performance, la maintenabilité et la sécurité du module reporting, veuillez respecter les directives suivantes lors de l'ajout ou de la modification de code :

### 3.1 Directives pour les Vues (Views)
1. **Sécurité et Contrôle d'Accès :**
   - Toujours utiliser le décorateur `@login_required`.
   - Si des groupes d'utilisateurs distincts existent (ex: `admin`, `commercial`), ajouter des vérifications de permissions (`@permission_required` ou `UserPassesTestMixin`) pour s'assurer que seuls les utilisateurs autorisés voient les rapports globaux.
2. **Optimisation des Requêtes (Agrégation dans la DB) :**
   - **Règle d'or :** Faire travailler la base de données, pas Python. 
   - Utiliser systématiquement les méthodes ORM `.annotate()`, `.aggregate()` associées à `Sum`, `Count`, `Avg`, et `TruncDate` pour les calculs.
   - Ne **JAMAIS** récupérer tous les objets avec `.all()` pour ensuite faire des boucles `for` en Python afin de calculer des totaux ou des compteurs. Cela provoquerait de graves problèmes de performance en production avec l'augmentation du volume de données.
3. **Optimisation des Requêtes (Relations ORM N+1) :**
   - Si vous devez itérer sur un `QuerySet` et accéder à des clés étrangères dans le template, utilisez toujours `.select_related()` (pour les relations OneToOne/ForeignKey) ou `.prefetch_related()` (pour ManyToMany/Reverse ForeignKey) afin d'éviter le problème des requêtes dites "N+1".
4. **Lisibilité et Structure :**
   - Préparer les données dans la vue et passer des structures prêtes à l'emploi (dictionnaires, listes calculées) au contexte. Le template HTML/Django ne doit faire que l'affichage, pas de logique métier complexe ni de formatage lourd.

### 3.2 Directives pour les Modèles (Models)
1. **Source de Vérité en Ligne (MVP) :**
   - Tant que les performances sont satisfaisantes, le reporting doit continuer d'interroger "à chaud" directement les modèles opérationnels source (`Commande`, `Client`, `Campagne`). Aucune table miroir ou entrepôt de données n'est requis à ce stade.
2. **Stratégie d'Optimisation (Passage à l'échelle) :**
   - Si les tableaux de bord deviennent trop lents lors de requêtes lourdes sur des millions d'enregistrements, privilégier la création de modèles spécifiques au reporting qui stockent des indicateurs pré-calculés (ex. `StatistiquesVentesJournalieres`).
   - Mettre à jour ces statistiques spécifiques par des tâches planifiées asynchrones (via `Celery` ou `Cron`) pendant la nuit, et ne faire lire à la vue de reporting que cette petite table de résultats agrégés.
3. **Indexation Stratégique :**
   - S'assurer que les champs fréquemment utilisés pour le filtrage dans le module de reporting, en particulier les dates (`date_commande`, `created_at`) et les statuts clés (`statut`, `actif`), bénéficient bien d'index dans leur modèle de de base (`db_index=True`).
