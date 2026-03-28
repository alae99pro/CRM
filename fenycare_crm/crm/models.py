"""
CRM models - Clients, Prospects, Interactions
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    """Modèle Client"""
    TYPE_CLIENT = [
        ('particulier', 'Particulier'),
        ('professionnel', 'Professionnel'),
        ('collectivite', 'Collectivité'),
        ('distributeur', 'Distributeur'),
        ('ambassadrice', 'Ambassadrice'),
    ]
    
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    pays = models.CharField(max_length=100, default='France')
    
    type_client = models.CharField(max_length=20, choices=TYPE_CLIENT, default='particulier')
    entreprise = models.CharField(max_length=200, blank=True, help_text="Nom de l'entreprise si professionnel")
    
    # Shopify
    shopify_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    
    # Métriques
    date_premier_achat = models.DateField(null=True, blank=True)
    nombre_achats = models.IntegerField(default=0)
    montant_total_achats = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Segmentation
    tags = models.CharField(max_length=500, blank=True, help_text="Tags séparés par des virgules")
    notes = models.TextField(blank=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients_crees')
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.prenom:
            return f"{self.prenom} {self.nom}"
        return self.nom
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}".strip() or self.nom


class Prospect(models.Model):
    """Modèle Prospect - Pipeline commercial"""
    STATUT_CHOICES = [
        ('prospect', 'Prospect'),
        ('en_cours', 'En cours'),
        ('gagne', 'Gagné'),
        ('perdu', 'Perdu'),
    ]
    
    SOURCE_CHOICES = [
        ('site_web', 'Site Web'),
        ('reseau_social', 'Réseau Social'),
        ('recommandation', 'Recommandation'),
        ('salon', 'Salon/Événement'),
        ('publicite', 'Publicité'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    entreprise = models.CharField(max_length=200, blank=True)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='prospect')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='site_web')
    
    # Pipeline
    montant_estime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    probabilite = models.IntegerField(default=50, help_text="Probabilité de conversion (0-100%)")
    date_conversion_prevue = models.DateField(null=True, blank=True)
    
    # Attribution
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prospects')
    
    # Conversion
    converti_en_client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='prospect_origine')
    date_conversion = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Prospect"
        verbose_name_plural = "Prospects"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_statut_display()}"
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}".strip() or self.nom
    
    def convertir_en_client(self, user=None):
        """Convertir le prospect en client"""
        if self.converti_en_client:
            return self.converti_en_client
        
        client = Client.objects.create(
            nom=self.nom,
            prenom=self.prenom,
            email=self.email,
            telephone=self.telephone,
            entreprise=self.entreprise,
            created_by=user,
        )
        
        self.converti_en_client = client
        self.statut = 'gagne'
        self.date_conversion = timezone.now()
        self.save()
        
        return client


class Interaction(models.Model):
    """Historique des interactions avec clients/prospects"""
    TYPE_INTERACTION = [
        ('appel', 'Appel téléphonique'),
        ('email', 'Email'),
        ('reunion', 'Réunion'),
        ('note', 'Note'),
        ('autre', 'Autre'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name='interactions')
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, null=True, blank=True, related_name='interactions')
    
    type_interaction = models.CharField(max_length=20, choices=TYPE_INTERACTION)
    sujet = models.CharField(max_length=200)
    description = models.TextField()
    
    date_interaction = models.DateTimeField(default=timezone.now)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Interaction"
        verbose_name_plural = "Interactions"
        ordering = ['-date_interaction']
    
    def __str__(self):
        target = self.client or self.prospect
        return f"{self.get_type_interaction_display()} - {target} - {self.date_interaction.strftime('%d/%m/%Y')}"
