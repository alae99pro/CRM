@echo off
echo ========================================
echo   FenyCare CRM - Script de demarrage
echo ========================================
echo.

REM Activer l'environnement virtuel
if exist "venv\Scripts\activate.bat" (
    echo [1/3] Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
) else (
    echo ERREUR: Environnement virtuel non trouve!
    echo Veuillez executer d'abord: python -m venv venv
    pause
    exit /b 1
)

echo.
echo [2/3] Verification de la base de donnees...
python manage.py migrate --noinput

echo.
echo [3/3] Demarrage du serveur Django...
echo.
echo ========================================
echo   Le CRM est pret!
echo   URL: http://127.0.0.1:8000
echo   Admin: http://127.0.0.1:8000/admin
echo.
echo   Login par defaut:
echo   - Username: admin
echo   - Password: admin123
echo ========================================
echo.

python manage.py runserver
