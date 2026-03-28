"""
Commande Django pour créer des données de test
Usage: python manage.py create_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from crm.models import Client, Prospect, Interaction
from supply_chain.models import Produit, Commande, LigneCommande
from marketing.models import Campagne, EmailEnvoye, SequenceEmail
from core.models import UserProfile


class Command(BaseCommand):
    help = 'Crée des données de démonstration pour le CRM'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Création des données de démonstration...'))
        
        # Créer des utilisateurs
        self.create_users()
        
        # Créer des clients
        self.create_clients()
        
        # Créer des prospects
        self.create_prospects()
        
        # Créer des produits
        self.create_produits()
        
        # Créer des commandes
        self.create_commandes()
        
        # Créer des campagnes
        self.create_campagnes()
        
        self.stdout.write(self.style.SUCCESS('✅ Données de démonstration créées avec succès!'))
        self.stdout.write('')
        self.stdout.write('📊 Résumé:')
        self.stdout.write(f'  - Utilisateurs: {User.objects.count()}')
        self.stdout.write(f'  - Clients: {Client.objects.count()}')
        self.stdout.write(f'  - Prospects: {Prospect.objects.count()}')
        self.stdout.write(f'  - Produits: {Produit.objects.count()}')
        self.stdout.write(f'  - Commandes: {Commande.objects.count()}')
        self.stdout.write(f'  - Campagnes: {Campagne.objects.count()}')

    def create_users(self):
        """Créer des utilisateurs de test"""
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@fenycare.com',
                password='admin123',
                first_name='Admin',
                last_name='FenyCare'
            )
            admin.profile.role = 'admin'
            admin.profile.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Utilisateur admin créé'))
        
        # Créer d'autres utilisateurs
        users_data = [
            {'username': 'commercial', 'role': 'commercial', 'first_name': 'Jean', 'last_name': 'Dupont'},
            {'username': 'marketing', 'role': 'marketing', 'first_name': 'Marie', 'last_name': 'Martin'},
        ]
        
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=f"{user_data['username']}@fenycare.com",
                    password='demo123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                user.profile.role = user_data['role']
                user.profile.save()
                self.stdout.write(f"  ✓ Utilisateur {user_data['username']} créé")

    def create_clients(self):
        """Créer des clients de test"""
        admin = User.objects.filter(username='admin').first()
        
        clients_data = [
            {
                'nom': 'Dubois', 'prenom': 'Sophie', 'email': 'sophie.dubois@email.com',
                'telephone': '0612345678', 'type_client': 'particulier',
                'ville': 'Paris', 'code_postal': '75001'
            },
            {
                'nom': 'Martin', 'prenom': 'Pierre', 'email': 'pierre.martin@email.com',
                'telephone': '0623456789', 'type_client': 'particulier',
                'ville': 'Lyon', 'code_postal': '69001'
            },
            {
                'nom': 'Crèche Les Bambins', 'prenom': '', 'email': 'contact@lesbambins.fr',
                'telephone': '0134567890', 'type_client': 'collectivite',
                'entreprise': 'Crèche Les Bambins', 'ville': 'Marseille', 'code_postal': '13001'
            },
            {
                'nom': 'École Maternelle Soleil', 'prenom': '', 'email': 'direction@ecole-soleil.fr',
                'telephone': '0145678901', 'type_client': 'professionnel',
                'entreprise': 'École Maternelle Soleil', 'ville': 'Toulouse', 'code_postal': '31000'
            },
            {
                'nom': 'Dupont', 'prenom': 'Claire', 'email': 'claire.dupont@email.com',
                'telephone': '0656789012', 'type_client': 'ambassadrice',
                'ville': 'Nantes', 'code_postal': '44000'
            },
        ]
        
        for data in clients_data:
            if not Client.objects.filter(email=data['email']).exists():
                client = Client.objects.create(
                    created_by=admin,
                    nombre_achats=random.randint(1, 10),
                    montant_total_achats=random.uniform(100, 5000),
                    **data
                )
                self.stdout.write(f"  ✓ Client {client.get_full_name()} créé")

    def create_prospects(self):
        """Créer des prospects de test"""
        user = User.objects.filter(username='commercial').first()
        
        prospects_data = [
            {
                'nom': 'Leclerc', 'prenom': 'Antoine', 'email': 'antoine.leclerc@email.com',
                'telephone': '0667890123', 'statut': 'prospect', 'source': 'site_web',
                'montant_estime': 500, 'probabilite': 30
            },
            {
                'nom': 'Bernard', 'prenom': 'Isabelle', 'email': 'isabelle.bernard@email.com',
                'telephone': '0678901234', 'statut': 'en_cours', 'source': 'recommandation',
                'montant_estime': 1200, 'probabilite': 70
            },
            {
                'nom': 'Petit', 'prenom': 'Thomas', 'email': 'thomas.petit@email.com',
                'telephone': '0689012345', 'statut': 'prospect', 'source': 'reseau_social',
                'montant_estime': 300, 'probabilite': 20
            },
            {
                'nom': 'Robert', 'prenom': 'Nathalie', 'email': 'nathalie.robert@email.com',
                'telephone': '0690123456', 'statut': 'gagne', 'source': 'salon',
                'montant_estime': 2000, 'probabilite': 100
            },
        ]
        
        for data in prospects_data:
            if not Prospect.objects.filter(email=data['email']).exists():
                prospect = Prospect.objects.create(responsable=user, **data)
                self.stdout.write(f"  ✓ Prospect {prospect.get_full_name()} créé")

    def create_produits(self):
        """Créer des produits de test"""
        produits_data = [
            {
                'nom': 'Meuble-lavabo Junior Bleu',
                'reference': 'MLJ-BLEU-001',
                'description': 'Meuble-lavabo ergonomique pour enfants 3-6 ans',
                'prix_unitaire': 299.99,
                'prix_achat': 150.00,
                'quantite_stock': 25,
                'seuil_alerte': 10
            },
            {
                'nom': 'Meuble-lavabo Junior Rose',
                'reference': 'MLJ-ROSE-001',
                'description': 'Meuble-lavabo ergonomique pour enfants 3-6 ans',
                'prix_unitaire': 299.99,
                'prix_achat': 150.00,
                'quantite_stock': 18,
                'seuil_alerte': 10
            },
            {
                'nom': 'Meuble-lavabo Junior Vert',
                'reference': 'MLJ-VERT-001',
                'description': 'Meuble-lavabo ergonomique pour enfants 3-6 ans',
                'prix_unitaire': 299.99,
                'prix_achat': 150.00,
                'quantite_stock': 30,
                'seuil_alerte': 10
            },
            {
                'nom': 'Kit Accessoires Hygiène',
                'reference': 'KIT-HYG-001',
                'description': 'Kit complet avec savon, serviette et miroir',
                'prix_unitaire': 49.99,
                'prix_achat': 25.00,
                'quantite_stock': 50,
                'seuil_alerte': 20
            },
            {
                'nom': 'Miroir de Sécurité Incassable',
                'reference': 'MIR-SEC-001',
                'description': 'Miroir incassable adapté aux enfants',
                'prix_unitaire': 29.99,
                'prix_achat': 15.00,
                'quantite_stock': 8,
                'seuil_alerte': 10
            },
        ]
        
        for data in produits_data:
            if not Produit.objects.filter(reference=data['reference']).exists():
                produit = Produit.objects.create(**data)
                self.stdout.write(f"  ✓ Produit {produit.nom} créé")

    def create_commandes(self):
        """Créer des commandes de test"""
        clients = Client.objects.all()[:5]
        produits = Produit.objects.all()
        
        statuts = ['en_attente', 'en_preparation', 'expediee', 'livree']
        
        for i, client in enumerate(clients):
            # Créer 2-3 commandes par client
            for j in range(random.randint(2, 3)):
                numero = f"CMD-2026-{1000 + i*10 + j}"
                if not Commande.objects.filter(numero_commande=numero).exists():
                    commande = Commande.objects.create(
                        numero_commande=numero,
                        client=client,
                        statut=random.choice(statuts),
                        date_commande=timezone.now() - timedelta(days=random.randint(1, 60)),
                        adresse_livraison=client.adresse or "123 Rue Example",
                        ville_livraison=client.ville or "Paris",
                        code_postal_livraison=client.code_postal or "75001",
                        frais_livraison=15.00
                    )
                    
                    # Ajouter 1-3 produits à la commande
                    nb_produits = random.randint(1, 3)
                    total = 0
                    for _ in range(nb_produits):
                        produit = random.choice(produits)
                        quantite = random.randint(1, 3)
                        ligne = LigneCommande.objects.create(
                            commande=commande,
                            produit=produit,
                            quantite=quantite,
                            prix_unitaire=produit.prix_unitaire
                        )
                        total += ligne.prix_total
                    
                    commande.montant_produits = total
                    commande.save()
                    
                    self.stdout.write(f"  ✓ Commande {numero} créée")

    def create_campagnes(self):
        """Créer des campagnes marketing de test"""
        campagnes_data = [
            {
                'nom': 'Lancement Nouvelle Collection',
                'type_campagne': 'newsletter',
                'statut': 'terminee',
                'description': 'Annonce de la nouvelle collection printemps',
                'sujet': '🌸 Découvrez notre nouvelle collection!',
                'segment': 'tous',
                'emails_envoyes': 150,
                'emails_ouverts': 95,
                'clics': 32
            },
            {
                'nom': 'Promotion Rentrée',
                'type_campagne': 'promotion',
                'statut': 'active',
                'description': 'Offre spéciale rentrée scolaire -15%',
                'sujet': '🎒 -15% pour la rentrée!',
                'segment': 'parents',
                'emails_envoyes': 200,
                'emails_ouverts': 120,
                'clics': 45
            },
            {
                'nom': 'Relance Panier Abandonné',
                'type_campagne': 'relance',
                'statut': 'active',
                'description': 'Relance automatique des paniers abandonnés',
                'sujet': 'Vous avez oublié quelque chose...',
                'segment': 'abandons',
                'emails_envoyes': 45,
                'emails_ouverts': 25,
                'clics': 12
            },
        ]
        
        for data in campagnes_data:
            if not Campagne.objects.filter(nom=data['nom']).exists():
                data['contenu_html'] = f"<h1>{data['sujet']}</h1><p>{data['description']}</p>"
                data['contenu_texte'] = f"{data['sujet']}\n\n{data['description']}"
                campagne = Campagne.objects.create(**data)
                self.stdout.write(f"  ✓ Campagne {campagne.nom} créée")
