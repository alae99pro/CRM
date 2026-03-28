import os
import django
from datetime import timedelta
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fenycare_crm.settings')
django.setup()

from django.utils import timezone
from supply_chain.models import Produit, Commande, LigneCommande
from crm.models import Client
from marketing.models import Campagne, EmailEnvoye

print("⚙️ CRÉATION DE DONNÉES DE TEST ⚙️")
print("====================================")

# 1. Vérifier qu'on a bien au moins un produit
produits = list(Produit.objects.all())
if not produits:
    print("📦 Création de 3 produits factices...")
    p1 = Produit.objects.create(nom="Crème Hydratante FenyCare", reference="CR-HYD-01", prix_unitaire=35.00, quantite_stock=100)
    p2 = Produit.objects.create(nom="Sérum Anti-Âge", reference="SER-AA-02", prix_unitaire=65.00, quantite_stock=50)
    p3 = Produit.objects.create(nom="Lotion Tonique", reference="LOT-TON-03", prix_unitaire=25.00, quantite_stock=200)
    produits = [p1, p2, p3]
else:
    print(f"✅ {len(produits)} produits existants trouvés.")

# 2. Vérifier qu'on a bien au moins un client
clients = list(Client.objects.all())
if not clients:
    print("👤 Création de 2 clients factices...")
    c1 = Client.objects.create(nom="Dupont", prenom="Marie", email="marie.dupont@email.com", type_client="particulier")
    c2 = Client.objects.create(nom="Pharmacie Centrale", prenom="Jean", email="contact@pharmacie.com", type_client="professionnel")
    clients = [c1, c2]
else:
    print(f"✅ {len(clients)} clients existants trouvés.")

# 3. Génération de quelques commandes aléatoires sur les 15 derniers jours
print("🛒 Génération de 5 commandes test (Statut 'Livrée')...")
for i in range(5):
    # Choisir un client et des dates au hasard
    client = random.choice(clients)
    jours_avant = random.randint(1, 15)
    date_cmd = timezone.now() - timedelta(days=jours_avant)
    
    # Créer la commande entête
    cmd = Commande.objects.create(
        numero_commande=f"CMD-TEST-{random.randint(1000, 9999)}",
        client=client,
        statut='livree',
        date_commande=date_cmd,
        frais_livraison=Decimal('5.00'),
        ville_livraison="Paris",
        code_postal_livraison="75000"
    )
    
    # Ajouter 1 à 3 lignes de produits à cette commande
    nb_lignes = random.randint(1, 3)
    produits_choisis = random.sample(produits, nb_lignes)
    montant_total_produits = 0
    
    for produit in produits_choisis:
        qt = random.randint(1, 4)
        prix_total_ligne = produit.prix_unitaire * qt
        montant_total_produits += prix_total_ligne
        
        LigneCommande.objects.create(
            commande=cmd,
            produit=produit,
            quantite=qt,
            prix_unitaire=produit.prix_unitaire,
            prix_total=prix_total_ligne
        )
        
    # Mettre à jour les totaux de la commande mère
    cmd.montant_produits = montant_total_produits
    cmd.montant_total = montant_total_produits + cmd.frais_livraison
    # Important: on ne déclenche pas le .save() simple pour auto_now_add si on veut garder la vieille date
    Commande.objects.filter(id=cmd.id).update(
        montant_produits=cmd.montant_produits, 
        montant_total=cmd.montant_total,
        date_commande=date_cmd
    )
    print(f"  - Commande {cmd.numero_commande} créée ({cmd.montant_total} €)")

# 4. Génération de campagnes marketing
print("\n📢 Génération de 2 Campagnes Marketing test...")
campagnes_types = ['newsletter', 'promotion', 'nouveau_produit']
for i in range(2):
    jours_avant = random.randint(5, 20)
    date_creation = timezone.now() - timedelta(days=jours_avant)
    
    envoyes = random.randint(200, 1500)
    ouverts = int(envoyes * random.uniform(0.15, 0.45))
    clics = int(ouverts * random.uniform(0.10, 0.30))
    conversions = int(clics * random.uniform(0.05, 0.15))
    
    c = Campagne.objects.create(
        nom=f"Campagne de Test {i+1} : {random.choice(['Soldes', 'Nouveau Sérum', 'Fidélité'])}",
        type_campagne=random.choice(campagnes_types),
        statut='terminee',
        emails_envoyes=envoyes,
        emails_ouverts=ouverts,
        clics=clics,
        conversions=conversions
    )
    # Update created_at
    Campagne.objects.filter(id=c.id).update(created_at=date_creation)
    
    print(f"  - Campagne '{c.nom}' créée ({envoyes} emails envoyés, {ouverts} ouverts)")
    
    # Créer quelques emails liés à cette campagne pour les clients existants
    for client in clients:
        # On suppose qu'ils l'ont reçu et peut-être ouvert
        ouvert = random.choice([True, False])
        EmailEnvoye.objects.create(
            campagne=c,
            client=client,
            type_email='marketing',
            statut='ouvert' if ouvert else 'envoye',
            sujet=f"Aperçu: {c.nom}",
            contenu="Contenu généré de test...",
            date_envoi=date_creation + timedelta(hours=1),
            date_ouverture=(date_creation + timedelta(days=1)) if ouvert else None
        )

print("\n🎉 Terminé ! Les données factices ont bien été écrites dans db.sqlite3.")
print("👉 Vous pouvez maintenant rafraîchir les pages de Reporting dans votre navigateur.")
