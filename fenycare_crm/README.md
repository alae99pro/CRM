# FenyCare CRM - MVP Sprint 3

## 📋 Description

CRM sur mesure pour FenyCare développé avec Django. Ce MVP inclut :

- ✅ Gestion Clients & Prospects (CRM)
- ✅ Pipeline commercial
- ✅ Gestion Produits & Commandes (Supply Chain)
- ✅ Alertes de stock
- ✅ Campagnes Marketing & Emails
- ✅ Reporting & Analytics
- ✅ Dashboard interactif

## 🎯 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- (Optionnel) MySQL/MariaDB pour la base de données

## 🚀 Installation sur Windows

### Étape 1 : Vérifier Python

Ouvrez PowerShell ou CMD et vérifiez :

```bash
python --version
# ou
python3 --version
```

Si Python n'est pas installé, téléchargez-le depuis https://www.python.org/downloads/

### Étape 2 : Créer un environnement virtuel

```bash
# Aller dans le dossier du projet
cd fenycare_crm

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Vous devriez voir (venv) au début de votre ligne de commande
```

### Étape 3 : Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** Si `mysqlclient` pose problème sur Windows, commentez cette ligne dans `requirements.txt` - SQLite sera utilisé par défaut.

### Étape 4 : Configurer l'environnement

```bash
# Copier le fichier d'exemple
copy .env.example .env

# Le fichier .env est déjà configuré pour SQLite par défaut
```

### Étape 5 : Initialiser la base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un super utilisateur
python manage.py createsuperuser
```

Quand demandé, entrez :
- Username: `admin`
- Email: `admin@fenycare.com`
- Password: `admin123` (ou votre choix)

### Étape 6 : Charger les données de démonstration (optionnel)

```bash
python manage.py loaddata demo_data.json
```

### Étape 7 : Lancer le serveur

```bash
python manage.py runserver
```

Le CRM sera accessible sur : http://127.0.0.1:8000

## 🔑 Connexion

- **URL:** http://127.0.0.1:8000
- **Username:** admin
- **Password:** admin123 (ou celui que vous avez choisi)

## 📁 Structure du Projet

```
fenycare_crm/
├── fenycare_crm/          # Configuration Django
│   ├── settings.py        # Paramètres
│   ├── urls.py           # URLs principales
│   └── wsgi.py
├── core/                 # App principale (Dashboard, Auth)
├── crm/                  # Gestion Clients & Prospects
├── supply_chain/         # Produits, Commandes, Stock
├── marketing/            # Campagnes, Emails
├── reporting/            # Rapports & Analytics
├── templates/            # Templates HTML
├── static/              # CSS, JS, Images
├── manage.py            # Script Django
└── requirements.txt     # Dépendances
```

## 🎨 Fonctionnalités Principales

### 1. Dashboard
- Vue d'ensemble des KPIs
- Statistiques en temps réel
- Activités récentes

### 2. CRM
- **Clients:** Gestion complète des clients
- **Prospects:** Pipeline commercial avec statuts
- **Interactions:** Historique des communications

### 3. Supply Chain
- **Produits:** Catalogue avec gestion de stock
- **Commandes:** Suivi des commandes
- **Alertes:** Notifications de stock bas

### 4. Marketing
- **Campagnes:** Création et suivi de campagnes
- **Emails:** Gestion des envois
- **Séquences:** Automatisations email

### 5. Reporting
- **Ventes:** Analyses des ventes
- **Clients:** Statistiques clients
- **Marketing:** Performance des campagnes
- **Stock:** État des stocks

## 🛠️ Commandes Utiles

```bash
# Activer l'environnement virtuel
venv\Scripts\activate

# Lancer le serveur
python manage.py runserver

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Accéder à l'admin Django
# URL: http://127.0.0.1:8000/admin

# Créer un nouvel utilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic
```

## 📊 Admin Django

L'interface d'administration Django est accessible sur :
http://127.0.0.1:8000/admin

Vous pouvez y gérer :
- Utilisateurs et permissions
- Tous les modèles (Clients, Produits, Commandes, etc.)
- Configuration système

## 🔧 Configuration Avancée

### Utiliser MySQL au lieu de SQLite

1. Installer MySQL sur Windows
2. Créer une base de données :
```sql
CREATE DATABASE fenycare_crm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Modifier `.env` :
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=fenycare_crm
DB_USER=root
DB_PASSWORD=votre_password
DB_HOST=localhost
DB_PORT=3306
```

4. Décommenter la configuration MySQL dans `settings.py`

### Emails

Pour activer les emails, configurez dans `.env` :
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password
```

## 🐛 Dépannage

### Erreur "No module named 'X'"
```bash
pip install -r requirements.txt
```

### Erreur de migration
```bash
python manage.py migrate --run-syncdb
```

### Port 8000 déjà utilisé
```bash
python manage.py runserver 8080
```

### Problème avec mysqlclient sur Windows
Commentez `mysqlclient==2.2.1` dans requirements.txt et utilisez SQLite

## 📝 Notes pour la Soutenance

### Points clés à démontrer :

1. **Architecture complète** : Modèle MVC Django avec 5 apps modulaires
2. **Base de données** : Modèles relationnels bien structurés
3. **Interface utilisateur** : Bootstrap 5, responsive, intuitive
4. **Fonctionnalités** : CRUD complet sur tous les modules
5. **Dashboard** : Visualisation des données en temps réel
6. **Admin Django** : Gestion avancée des données

### Données de test à créer :

- 10-15 clients de différents types
- 5-10 prospects avec différents statuts
- 5-10 produits avec stocks variés
- 10+ commandes avec différents statuts
- 2-3 campagnes marketing

## 👥 Équipe Projet

- Alae MOUADEN
- Salaheddine SALIMI
- Salaheddine AITOUAHMAN
- Amjad DOURI
- Bilal CHAOUI

**Cliente:** Yassmina El Fenen
**Encadrant:** M. Thierry Hamon




