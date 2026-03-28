import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fenycare_crm.settings')
django.setup()

from supply_chain.models import Produit, Commande, LigneCommande
from crm.models import Client
from marketing.models import Campagne, EmailEnvoye

print("🧹 DÉMARRAGE DU NETTOYAGE DES DONNÉES DE TEST 🧹")
print("==================================================")

# 1. Supprimer les commandes de test (On les a nommées CMD-TEST-XXXX)
commandes_test = Commande.objects.filter(numero_commande__startswith='CMD-TEST-')
nb_commandes = commandes_test.count()

if nb_commandes > 0:
    print(f"🗑️ {nb_commandes} commandes de test trouvées. Suppression en cours...")
    # La suppression en cascade supprimera automatiquement les LigneCommande associées
    commandes_test.delete()
    print("✅ Les commandes et leurs lignes associées ont été supprimées.")
else:
    print("🤷‍♂️ Aucune commande de test trouvée à supprimer.")

# 2. Supprimer les clients factices (Optionnel - On recherche les prénoms ou emails spécifiques)
clients_test = Client.objects.filter(nom__in=["Dupont", "Pharmacie Centrale"], prenom__in=["Marie", "Jean"])
nb_clients = clients_test.count()

if nb_clients > 0:
    print(f"🗑️ {nb_clients} clients de test trouvés.")
    clients_test.delete()
    print("✅ Les clients factices ont été supprimés.")
else:
    print("🤷‍♂️ Aucun client factice à supprimer.")

# 3. Supprimer les produits factices
produits_test = Produit.objects.filter(reference__startswith="CR-HYD-01") | Produit.objects.filter(reference__startswith="SER-AA-02") | Produit.objects.filter(reference__startswith="LOT-TON-03")
nb_produits = produits_test.count()

if nb_produits > 0:
    print(f"🗑️ {nb_produits} produits de test trouvés.")
    produits_test.delete()
    print("✅ Les produits factices ont été supprimés.")
else:
    print("🤷‍♂️ Aucun produit factice à supprimer.")

# 4. Supprimer les Campagnes Marketing
campagnes_test = Campagne.objects.filter(nom__startswith="Campagne de Test")
nb_campagnes = campagnes_test.count()

if nb_campagnes > 0:
    print(f"🗑️ {nb_campagnes} campagnes de test trouvées.")
    # La suppression en cascade effacera aussi les EmailEnvoye associés
    campagnes_test.delete()
    print("✅ Les campagnes factices et les emails ont été supprimés.")
else:
    print("🤷‍♂️ Aucune campagne de test à supprimer.")

print("\n🎉 Nettoyage terminé ! Votre base de données est revenue à la normale.")
