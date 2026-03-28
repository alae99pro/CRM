import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fenycare_crm.settings')
django.setup()

from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client
from django.contrib.auth.models import User

user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.first()

client = Client()

try:
    from core.models import UserProfile
    if not hasattr(user, 'profile') or not user.profile:
        UserProfile.objects.create(user=user)
except:
    try:
        from core.models import Profile
        if not hasattr(user, 'profile') or not user.profile:
            Profile.objects.create(user=user)
    except:
        pass

client.force_login(user)

urls_to_test = [
    ('/reporting/ventes/', 'Ventes'),
    ('/reporting/clients/', 'Clients'),
    ('/reporting/marketing/', 'Marketing'),
    ('/reporting/stock/', 'Stock'),
]

print("🔍 DÉBUT DE LA VÉRIFICATION DES RAPPORTS ET TEMPLATES\n")

for url, name in urls_to_test:
    print(f"--- Rapport : {name} ---")
    response = client.get(url)
    
    if response.status_code != 200:
        print(f"  ❌ Erreur: {response.status_code}")
        print(response.content.decode('utf-8')[:200]) # Afficher un bout de l'erreur
        continue
        
    print(f"  ✅ Status 200 OK")
    
    html = response.content.decode('utf-8')
    
    if 'stats' in response.context:
        stats = response.context['stats']
        print(f"  📊 Variables du contexte backend :")
        
        erreurs = 0
        for cle, valeur in stats.items():
            print(f"    • {cle}: {valeur}")
            
            val_str = str(valeur)
            if isinstance(valeur, Decimal) or isinstance(valeur, float):
                val_str = str(int(valeur))

            if val_str not in html:
                print(f"    ⚠️ Attention: La valeur '{val_str}' n'a pas été trouvée explicitement dans le HTML rendu.")
                erreurs += 1
                
        if erreurs == 0:
            print("  ✅ Le backend transmet bien ces données et le template les affiche sans erreur fatale.")
    print()

print("🏁 FIN DES TESTS")
