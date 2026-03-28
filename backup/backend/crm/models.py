from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


# SECTION 1: UTILISATEURS ET SéCURITé

class User(AbstractUser):
    """Utilisateur du systéme CRM"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('commercial', 'Commercial'),
        ('marketing', 'Marketing'),
        ('logistique', 'Logistique'),
        ('direction', 'Direction'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='commercial',
        verbose_name='Réle'
    )
    telephone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Permission(models.Model):
    """Permission d'accés aux fonctionnalités"""
    
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'permission'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class UserPermission(models.Model):
    """Relation entre utilisateur et permissions"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_permission'
        unique_together = ['user', 'permission']
        verbose_name = 'Permission utilisateur'
        verbose_name_plural = 'Permissions utilisateurs'


class AuditLog(models.Model):
    """Journal d'audit pour la traéabilité RGPD"""
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    table_name = models.CharField(max_length=50, blank=True, null=True)
    record_id = models.IntegerField(null=True, blank=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Journal d\'audit'
        verbose_name_plural = 'Journaux d\'audit'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['table_name', 'record_id']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.user} - {self.created_at}"


# SECTION 2: MODULE CRM

class Prospect(models.Model):
    """Client ou prospect"""
    
    TYPE_CLIENT_CHOICES = [
        ('particulier', 'Particulier'),
        ('professionnel', 'Professionnel'),
    ]
    
    STATUT_CHOICES = [
        ('prospect', 'Prospect'),
        ('en_cours', 'En cours'),
        ('gagne', 'Gagné'),
        ('perdu', 'Perdu'),
    ]
    
    SEGMENT_CHOICES = [
        ('parents', 'Parents'),
        ('collectivites', 'Collectivités'),
        ('distributeurs', 'Distributeurs'),
        ('ambassadrices', 'Ambassadrices'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    entreprise = models.CharField(max_length=150, blank=True, null=True)
    type_client = models.CharField(max_length=20, choices=TYPE_CLIENT_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='prospect')
    segment = models.CharField(max_length=20, choices=SEGMENT_CHOICES, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True, help_text="Origine du contact")
    adresse = models.TextField(blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    pays = models.CharField(max_length=50, default='France')
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score de qualification (0-100)"
    )
    notes = models.TextField(blank=True, null=True)
    consentement_rgpd = models.BooleanField(default=False)
    date_consentement = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prospect'
        verbose_name = 'Prospect'
        verbose_name_plural = 'Prospects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['statut']),
            models.Index(fields=['segment']),
            models.Index(fields=['type_client']),
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


class Interaction(models.Model):
    """Historique des interactions avec les prospects"""
    
    TYPE_CHOICES = [
        ('appel', 'Appel téléphonique'),
        ('email', 'Email'),
        ('reunion', 'Réunion'),
        ('note', 'Note'),
        ('sms', 'SMS'),
        ('visite', 'Visite'),
    ]
    
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('complete', 'Complété'),
        ('annule', 'Annulé'),
    ]
    
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type_interaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    sujet = models.CharField(max_length=255)
    contenu = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='complete')
    date_interaction = models.DateTimeField()
    duree_minutes = models.IntegerField(null=True, blank=True)
    resultat = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'interaction'
        verbose_name = 'Interaction'
        verbose_name_plural = 'Interactions'
        ordering = ['-date_interaction']
        indexes = [
            models.Index(fields=['prospect', 'date_interaction']),
            models.Index(fields=['type_interaction']),
        ]
    
    def __str__(self):
        return f"{self.get_type_interaction_display()} - {self.prospect} - {self.date_interaction}"


class Opportunite(models.Model):
    """Opportunité commerciale (pipeline)"""
    
    ETAPE_CHOICES = [
        ('qualification', 'Qualification'),
        ('proposition', 'Proposition'),
        ('negociation', 'Négociation'),
        ('cloture', 'Cléture'),
    ]
    
    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('gagne', 'Gagné'),
        ('perdu', 'Perdu'),
        ('suspendu', 'Suspendu'),
    ]
    
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='opportunites')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    montant_estime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    probabilite = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    etape = models.CharField(max_length=20, choices=ETAPE_CHOICES, default='qualification')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouvert')
    date_cloture_prevue = models.DateField(null=True, blank=True)
    date_cloture_effective = models.DateField(null=True, blank=True)
    raison_perte = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'opportunite'
        verbose_name = 'Opportunité'
        verbose_name_plural = 'Opportunités'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['prospect', 'statut']),
            models.Index(fields=['etape']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.prospect}"


# SECTION 3: MODULE SUPPLY CHAIN

class Produit(models.Model):
    """Produit FenyCare"""
    
    shopify_product_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_actuel = models.IntegerField(default=0)
    seuil_alerte = models.IntegerField(default=10)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    poids = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Poids en kg")
    dimensions = models.CharField(max_length=50, blank=True, null=True, help_text="LxlxH en cm")
    image_url = models.URLField(max_length=500, blank=True, null=True)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'produit'
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['nom']
        indexes = [
            models.Index(fields=['shopify_product_id']),
            models.Index(fields=['sku']),
            models.Index(fields=['stock_actuel']),
        ]
    
    def __str__(self):
        return f"{self.nom} ({self.sku})"
    
    @property
    def est_en_alerte(self):
        return self.stock_actuel <= self.seuil_alerte


class Commande(models.Model):
    """Commande client"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('preparation', 'En préparation'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]
    
    PAIEMENT_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('virement', 'Virement'),
        ('paypal', 'PayPal'),
        ('autre', 'Autre'),
    ]
    
    STATUT_PAIEMENT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('rembourse', 'Remboursé'),
        ('echoue', 'échoué'),
    ]
    
    shopify_order_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    numero_commande = models.CharField(max_length=50, unique=True)
    prospect = models.ForeignKey(Prospect, on_delete=models.PROTECT, related_name='commandes')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2)
    montant_tva = models.DecimalField(max_digits=10, decimal_places=2)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    frais_livraison = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mode_paiement = models.CharField(max_length=20, choices=PAIEMENT_CHOICES, null=True, blank=True)
    statut_paiement = models.CharField(max_length=20, choices=STATUT_PAIEMENT_CHOICES, default='en_attente')
    adresse_livraison = models.TextField(blank=True, null=True)
    adresse_facturation = models.TextField(blank=True, null=True)
    date_commande = models.DateTimeField()
    date_expedition = models.DateTimeField(null=True, blank=True)
    date_livraison = models.DateTimeField(null=True, blank=True)
    numero_suivi = models.CharField(max_length=100, blank=True, null=True)
    transporteur = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'commande'
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_commande']
        indexes = [
            models.Index(fields=['shopify_order_id']),
            models.Index(fields=['numero_commande']),
            models.Index(fields=['prospect', 'date_commande']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"{self.numero_commande} - {self.prospect}"
    
    def save(self, *args, **kwargs):
        if not self.numero_commande:
            # Générer un numéro de commande automatique
            from datetime import datetime
            now = datetime.now()
            count = Commande.objects.filter(
                date_commande__year=now.year,
                date_commande__month=now.month
            ).count() + 1
            self.numero_commande = f"CMD-{now.strftime('%Y%m')}-{count:05d}"
        super().save(*args, **kwargs)


class LigneCommande(models.Model):
    """Ligne de commande (détail des produits)"""
    
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Remise en %")
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ligne_commande'
        verbose_name = 'Ligne de commande'
        verbose_name_plural = 'Lignes de commande'
        indexes = [
            models.Index(fields=['commande']),
            models.Index(fields=['produit']),
        ]
    
    def __str__(self):
        return f"{self.produit} x{self.quantite}"
    
    def save(self, *args, **kwargs):
        # Calcul automatique du sous-total
        self.sous_total = self.quantite * self.prix_unitaire * (1 - self.remise / 100)
        super().save(*args, **kwargs)


class MouvementStock(models.Model):
    """Mouvement de stock"""
    
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('ajustement', 'Ajustement'),
        ('retour', 'Retour'),
    ]
    
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.IntegerField()
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    motif = models.CharField(max_length=255, blank=True, null=True)
    date_mouvement = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mouvement_stock'
        verbose_name = 'Mouvement de stock'
        verbose_name_plural = 'Mouvements de stock'
        ordering = ['-date_mouvement']
        indexes = [
            models.Index(fields=['produit', 'date_mouvement']),
            models.Index(fields=['type_mouvement']),
        ]
    
    def __str__(self):
        return f"{self.get_type_mouvement_display()} - {self.produit} - {self.quantite}"


class Fournisseur(models.Model):
    """Fournisseur"""
    
    FIABILITE_CHOICES = [
        ('excellent', 'Excellent'),
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('faible', 'Faible'),
    ]
    
    nom = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    delai_livraison_jours = models.IntegerField(null=True, blank=True)
    fiabilite = models.CharField(max_length=20, choices=FIABILITE_CHOICES, default='bon')
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'fournisseur'
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class BonCommandeFournisseur(models.Model):
    """Bon de commande fournisseur"""
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('confirme', 'Confirmé'),
        ('recu', 'Reéu'),
        ('annule', 'Annulé'),
    ]
    
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT, related_name='bons_commande')
    numero_bon = models.CharField(max_length=50, unique=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_commande = models.DateField(null=True, blank=True)
    date_livraison_prevue = models.DateField(null=True, blank=True)
    date_livraison_effective = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bon_commande_fournisseur'
        verbose_name = 'Bon de commande fournisseur'
        verbose_name_plural = 'Bons de commande fournisseurs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['fournisseur', 'statut']),
        ]
    
    def __str__(self):
        return f"{self.numero_bon} - {self.fournisseur}"


class LigneBonCommandeFournisseur(models.Model):
    """Ligne de bon de commande fournisseur"""
    
    bon_commande = models.ForeignKey(BonCommandeFournisseur, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'ligne_bon_commande_fournisseur'
        verbose_name = 'Ligne bon commande fournisseur'
        verbose_name_plural = 'Lignes bon commande fournisseur'
    
    def __str__(self):
        return f"{self.produit} x{self.quantite}"
    
    def save(self, *args, **kwargs):
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)


# SECTION 4: MODULE MARKETING

class Segment(models.Model):
    """Segment de clients"""
    
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    criteres = models.JSONField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'segment'
        verbose_name = 'Segment'
        verbose_name_plural = 'Segments'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class ProspectSegment(models.Model):
    """Relation N-N entre Prospect et Segment"""
    
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prospect_segment'
        unique_together = ['prospect', 'segment']
        verbose_name = 'Prospect-Segment'
        verbose_name_plural = 'Prospects-Segments'


class Campagne(models.Model):
    """Campagne marketing"""
    
    TYPE_CHOICES = [
        ('newsletter', 'Newsletter'),
        ('relance', 'Relance'),
        ('bienvenue', 'Bienvenue'),
        ('promo', 'Promotion'),
        ('panier_abandonne', 'Panier abandonné'),
    ]
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('programmee', 'Programmée'),
        ('en_cours', 'En cours'),
        ('envoyee', 'Envoyée'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    nom = models.CharField(max_length=255)
    type_campagne = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    objet_email = models.CharField(max_length=255, blank=True, null=True)
    contenu_html = models.TextField(blank=True, null=True)
    contenu_text = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    nombre_destinataires = models.IntegerField(default=0)
    nombre_envoyes = models.IntegerField(default=0)
    nombre_ouverts = models.IntegerField(default=0)
    nombre_clics = models.IntegerField(default=0)
    nombre_conversions = models.IntegerField(default=0)
    taux_ouverture = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    taux_clic = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    taux_conversion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    segments = models.ManyToManyField(Segment, through='CampagneSegment', related_name='campagnes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'campagne'
        verbose_name = 'Campagne'
        verbose_name_plural = 'Campagnes'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['type_campagne', 'statut']),
            models.Index(fields=['date_envoi']),
        ]
    
    def __str__(self):
        return f"{self.nom} ({self.get_type_campagne_display()})"


class CampagneSegment(models.Model):
    """Relation N-N entre Campagne et Segment"""
    
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'campagne_segment'
        unique_together = ['campagne', 'segment']


class Email(models.Model):
    """Email envoyé"""
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('envoye', 'Envoyé'),
        ('echec', 'échec'),
        ('bounce', 'Bounce'),
    ]
    
    campagne = models.ForeignKey(Campagne, on_delete=models.SET_NULL, null=True, blank=True, related_name='emails')
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name='emails')
    objet = models.CharField(max_length=255)
    contenu_html = models.TextField(blank=True, null=True)
    contenu_text = models.TextField(blank=True, null=True)
    statut_envoi = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_ouverture = models.DateTimeField(null=True, blank=True)
    nombre_ouvertures = models.IntegerField(default=0)
    nombre_clics = models.IntegerField(default=0)
    erreur_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'email'
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campagne', 'statut_envoi']),
            models.Index(fields=['prospect']),
        ]
    
    def __str__(self):
        return f"{self.objet} - {self.prospect.email}"


class EmailStatistique(models.Model):
    """Statistiques de tracking des emails"""
    
    TYPE_EVENT_CHOICES = [
        ('ouverture', 'Ouverture'),
        ('clic', 'Clic'),
        ('bounce', 'Bounce'),
        ('spam', 'Spam'),
        ('desinscription', 'Désinscription'),
    ]
    
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='statistiques')
    type_event = models.CharField(max_length=20, choices=TYPE_EVENT_CHOICES)
    lien_clique = models.URLField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    date_event = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'email_statistique'
        verbose_name = 'Statistique email'
        verbose_name_plural = 'Statistiques emails'
        ordering = ['-date_event']
        indexes = [
            models.Index(fields=['email', 'type_event']),
        ]
    
    def __str__(self):
        return f"{self.get_type_event_display()} - {self.email}"


class SequenceEmail(models.Model):
    """Séquence d'emails automatisés"""
    
    DECLENCHEUR_CHOICES = [
        ('inscription', 'Inscription'),
        ('achat', 'Achat'),
        ('panier_abandonne', 'Panier abandonné'),
        ('anniversaire', 'Anniversaire'),
        ('inactivite', 'Inactivité'),
    ]
    
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    declencheur = models.CharField(max_length=20, choices=DECLENCHEUR_CHOICES)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sequence_email'
        verbose_name = 'Séquence email'
        verbose_name_plural = 'Séquences emails'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class EtapeSequence(models.Model):
    """étape d'une séquence email"""
    
    sequence = models.ForeignKey(SequenceEmail, on_delete=models.CASCADE, related_name='etapes')
    ordre = models.IntegerField()
    delai_jours = models.IntegerField(default=0)
    delai_heures = models.IntegerField(default=0)
    objet = models.CharField(max_length=255)
    contenu_html = models.TextField(blank=True, null=True)
    contenu_text = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'etape_sequence'
        verbose_name = 'étape de séquence'
        verbose_name_plural = 'étapes de séquences'
        ordering = ['sequence', 'ordre']
        unique_together = ['sequence', 'ordre']
    
    def __str__(self):
        return f"{self.sequence} - étape {self.ordre}"


# SECTION 5: MODULE REPORTING

class Dashboard(models.Model):
    """Tableau de bord personnalisé"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    nom = models.CharField(max_length=150)
    configuration = models.JSONField(null=True, blank=True)
    est_defaut = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dashboard'
        verbose_name = 'Tableau de bord'
        verbose_name_plural = 'Tableaux de bord'
        ordering = ['-est_defaut', 'nom']
    
    def __str__(self):
        return f"{self.nom} - {self.user}"


class KPI(models.Model):
    """Indicateur de performance"""
    
    TYPE_CHOICES = [
        ('ventes', 'Ventes'),
        ('marketing', 'Marketing'),
        ('commercial', 'Commercial'),
        ('stock', 'Stock'),
        ('satisfaction', 'Satisfaction'),
    ]
    
    PERIODE_CHOICES = [
        ('jour', 'Jour'),
        ('semaine', 'Semaine'),
        ('mois', 'Mois'),
        ('trimestre', 'Trimestre'),
        ('annee', 'Année'),
    ]
    
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    valeur = models.DecimalField(max_digits=15, decimal_places=2)
    unite = models.CharField(max_length=20, blank=True, null=True)
    type_kpi = models.CharField(max_length=20, choices=TYPE_CHOICES)
    periode = models.CharField(max_length=20, choices=PERIODE_CHOICES)
    date_calcul = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'kpi'
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
        ordering = ['-date_calcul']
        indexes = [
            models.Index(fields=['type_kpi', 'periode', 'date_calcul']),
        ]
    
    def __str__(self):
        return f"{self.nom} - {self.valeur} {self.unite or ''}"


class Rapport(models.Model):
    """Rapport généré"""
    
    TYPE_CHOICES = [
        ('ventes', 'Ventes'),
        ('stock', 'Stock'),
        ('campagne', 'Campagne'),
        ('pipeline', 'Pipeline'),
        ('personnalise', 'Personnalisé'),
    ]
    
    nom = models.CharField(max_length=255)
    type_rapport = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    parametres = models.JSONField(null=True, blank=True)
    fichier_path = models.CharField(max_length=500, blank=True, null=True)
    genere_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_generation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rapport'
        verbose_name = 'Rapport'
        verbose_name_plural = 'Rapports'
        ordering = ['-date_generation']
        indexes = [
            models.Index(fields=['type_rapport', 'date_generation']),
        ]
    
    def __str__(self):
        return f"{self.nom} - {self.date_generation}"


# SECTION 6: TABLES SYSTéME

class Settings(models.Model):
    """Paramétres systéme"""
    
    TYPE_CHOICES = [
        ('string', 'Chaéne'),
        ('number', 'Nombre'),
        ('boolean', 'Booléen'),
        ('json', 'JSON'),
    ]
    
    cle = models.CharField(max_length=100, unique=True)
    valeur = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='string')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'settings'
        verbose_name = 'Paramétre'
        verbose_name_plural = 'Paramétres'
        ordering = ['cle']
    
    def __str__(self):
        return f"{self.cle} = {self.valeur}"


class SyncShopify(models.Model):
    """Log de synchronisation Shopify"""
    
    TYPE_CHOICES = [
        ('produit', 'Produit'),
        ('commande', 'Commande'),
        ('client', 'Client'),
        ('stock', 'Stock'),
    ]
    
    STATUT_CHOICES = [
        ('success', 'Succés'),
        ('error', 'Erreur'),
        ('pending', 'En attente'),
    ]
    
    type_sync = models.CharField(max_length=20, choices=TYPE_CHOICES)
    shopify_id = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    message = models.TextField(blank=True, null=True)
    date_sync = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sync_shopify'
        verbose_name = 'Sync Shopify'
        verbose_name_plural = 'Syncs Shopify'
        ordering = ['-date_sync']
        indexes = [
            models.Index(fields=['type_sync', 'statut']),
        ]
    
    def __str__(self):
        return f"{self.get_type_sync_display()} - {self.get_statut_display()}"


class CeleryTask(models.Model):
    """Téche Celery"""
    
    STATUT_CHOICES = [
        ('pending', 'En attente'),
        ('started', 'Démarré'),
        ('success', 'Succés'),
        ('failure', 'échec'),
        ('retry', 'Nouvelle tentative'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True)
    nom_task = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='pending')
    resultat = models.TextField(blank=True, null=True)
    erreur = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_execution = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'celery_task'
        verbose_name = 'Téche Celery'
        verbose_name_plural = 'Téches Celery'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['task_id']),
            models.Index(fields=['statut']),
        ]
    
    def __str__(self):
        return f"{self.nom_task} - {self.get_statut_display()}"