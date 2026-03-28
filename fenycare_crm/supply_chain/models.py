"""
Supply Chain models - Produits, Commandes, Stock
"""
from django.db import models
from django.utils import timezone
from crm.models import Client


class Produit(models.Model):
    """Modèle Produit"""
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=100, unique=True)
    
    # Prix
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Stock
    quantite_stock = models.IntegerField(default=0)
    seuil_alerte = models.IntegerField(default=10, help_text="Seuil minimum avant alerte")
    
    # Shopify
    shopify_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    shopify_variant_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Images
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    
    # Statut
    actif = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.reference})"
    
    @property
    def stock_bas(self):
        """Vérifie si le stock est en dessous du seuil"""
        return self.quantite_stock <= self.seuil_alerte
    
    @property
    def valeur_stock(self):
        """Calcule la valeur totale du stock"""
        return self.quantite_stock * self.prix_unitaire


class Commande(models.Model):
    """Modèle Commande"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_preparation', 'En préparation'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    
    numero_commande = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='commandes')
    
    date_commande = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    # Montants
    montant_produits = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Livraison
    adresse_livraison = models.TextField()
    ville_livraison = models.CharField(max_length=100)
    code_postal_livraison = models.CharField(max_length=10)
    pays_livraison = models.CharField(max_length=100, default='France')
    
    # Suivi
    numero_suivi = models.CharField(max_length=200, blank=True)
    transporteur = models.CharField(max_length=100, blank=True)
    date_expedition = models.DateTimeField(null=True, blank=True)
    date_livraison = models.DateTimeField(null=True, blank=True)
    
    # Shopify
    shopify_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande']
    
    def __str__(self):
        return f"Commande {self.numero_commande} - {self.client.get_full_name()}"
    
    def save(self, *args, **kwargs):
        """Calcule le montant total avant sauvegarde"""
        self.montant_total = self.montant_produits + self.frais_livraison
        super().save(*args, **kwargs)


class LigneCommande(models.Model):
    """Ligne de commande - Produits dans une commande"""
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    
    quantite = models.IntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
    
    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"
    
    def save(self, *args, **kwargs):
        """Calcule le prix total avant sauvegarde"""
        self.prix_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)


class AlerteStock(models.Model):
    """Alertes de stock bas"""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='alertes')
    quantite_actuelle = models.IntegerField()
    seuil = models.IntegerField()
    
    resolu = models.BooleanField(default=False)
    date_resolution = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Alerte stock"
        verbose_name_plural = "Alertes stock"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Alerte - {self.produit.nom} (Stock: {self.quantite_actuelle})"
