@echo off
echo ========================================
echo   FenyCare CRM - Installation
echo ========================================
echo.

echo [1/6] Creation de l'environnement virtuel...
python -m venv venv
if errorlevel 1 (
    echo ERREUR: Impossible de creer l'environnement virtuel
    echo Verifiez que Python est installe correctement
    pause
    exit /b 1
)

echo.
echo [2/6] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo [3/6] Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo [4/6] Installation des dependances...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ATTENTION: Certaines dependances ont echoue
    echo Si mysqlclient pose probleme, SQLite sera utilise
    echo.
)

echo.
echo [5/6] Copie du fichier de configuration...
if not exist ".env" (
    copy .env.example .env
    echo Fichier .env cree avec succes
) else (
    echo Fichier .env existe deja
)

echo.
echo [6/6] Creation de la base de donnees...
python manage.py migrate
if errorlevel 1 (
    echo ERREUR lors de la creation de la base de donnees
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation terminee avec succes!
echo ========================================
echo.
echo Prochaines etapes:
echo.
echo 1. Creer un super utilisateur:
echo    python manage.py createsuperuser
echo.
echo 2. Lancer le serveur:
echo    python manage.py runserver
echo    ou double-cliquer sur start.bat
echo.
echo ========================================

pause
