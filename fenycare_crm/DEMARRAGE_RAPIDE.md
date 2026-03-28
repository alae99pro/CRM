# 🚀 Guide de Démarrage Rapide - FenyCare CRM

## Installation Express (5 minutes)

### Option 1 : Installation Automatique (Recommandé)

1. **Double-cliquez sur `install.bat`**
   - Le script va tout installer automatiquement

2. **Créez un administrateur :**
   ```bash
   python manage.py createsuperuser
   ```
   - Username: `admin`
   - Email: `admin@fenycare.com`  
   - Password: `admin123`

3. **Chargez les données de test (optionnel) :**
   ```bash
   python manage.py create_demo_data
   ```

4. **Double-cliquez sur `start.bat`** pour lancer le serveur

5. **Ouvrez votre navigateur :**
   - http://127.0.0.1:8000

---

### Option 2 : Installation Manuelle

Si les fichiers .bat ne fonctionnent pas, suivez ces étapes :

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement (Windows)
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Copier la configuration
copy .env.example .env

# 5. Créer la base de données
python manage.py migrate

# 6. Créer un administrateur
python manage.py createsuperuser

# 7. Charger les données de test
python manage.py create_demo_data

# 8. Lancer le serveur
python manage.py runserver
```

---

## 🎯 Accès au CRM

**URL principale :** http://127.0.0.1:8000

**Login par défaut :**
- Username: `admin`
- Password: `admin123`

**Admin Django :** http://127.0.0.1:8000/admin

---

## 📱 Menu Principal

Après connexion, vous avez accès à :

### 🏠 Dashboard
- Vue d'ensemble des KPIs
- Statistiques en temps réel
- Dernières activités

### 👥 CRM
- **Clients** : Liste et gestion des clients
- **Prospects** : Pipeline commercial

### 📦 Supply Chain
- **Produits** : Catalogue et stocks
- **Commandes** : Suivi des commandes
- **Alertes Stock** : Notifications

### 📧 Marketing
- **Campagnes** : Gestion des campagnes
- **Emails** : Historique des envois
- **Séquences** : Automatisations

### 📊 Reporting
- **Ventes** : Analyses des ventes
- **Clients** : Statistiques clients
- **Marketing** : Performance
- **Stock** : État des stocks

---

## ✅ Vérification de l'Installation

Pour vérifier que tout fonctionne :

1. ✅ Le serveur démarre sans erreur
2. ✅ Vous pouvez vous connecter
3. ✅ Le dashboard s'affiche
4. ✅ Les menus sont accessibles
5. ✅ L'admin Django fonctionne

---

## 🛠️ Commandes Utiles

```bash
# Activer l'environnement
venv\Scripts\activate

# Lancer le serveur
python manage.py runserver

# Créer des données de test
python manage.py create_demo_data

# Créer un nouvel utilisateur
python manage.py createsuperuser

# Réinitialiser la base de données
python manage.py flush
python manage.py migrate
python manage.py create_demo_data
```

---

## 🐛 Problèmes Courants

### Le serveur ne démarre pas
```bash
# Vérifier que l'environnement est activé
venv\Scripts\activate

# Vérifier les migrations
python manage.py migrate
```

### Erreur "Module not found"
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

### Port 8000 déjà utilisé
```bash
# Utiliser un autre port
python manage.py runserver 8080
```

---

## 📝 Pour la Soutenance

### Préparez ces éléments :

1. **Démonstration du CRM fonctionnel**
   - Dashboard avec données
   - Navigation dans les modules
   - Création/Modification d'entités

2. **Points techniques à présenter**
   - Architecture Django MVC
   - Modèles de données (5 apps)
   - Interface Bootstrap responsive
   - Admin Django

3. **Données de démonstration**
   - 10-15 clients variés
   - 5-10 prospects
   - 5+ produits
   - 10+ commandes
   - 2-3 campagnes marketing

### Commandes pour la démo :

```bash
# Lancer le serveur pour la démo
python manage.py runserver

# Ouvrir plusieurs onglets :
# - Dashboard : http://127.0.0.1:8000
# - Clients : http://127.0.0.1:8000/crm/clients/
# - Produits : http://127.0.0.1:8000/supply-chain/produits/
# - Admin : http://127.0.0.1:8000/admin
```

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez que Python 3.10+ est installé
2. Vérifiez que l'environnement virtuel est activé
3. Consultez les logs dans la console
4. Vérifiez le fichier `.env`

---

## 🎓 Bon courage pour votre soutenance !

**Équipe :** Alae MOUADEN, Salaheddine SALIMI, Salaheddine AITOUAHMANE, Amjad DOURI, Bilal CHAOUI

**Cliente :** Yassmina El Fenen

**Sprint 3 - MVP - Février 2026**
