"""
Marketing models - Campagnes, Emails, Statistiques
"""
from django.db import models
from django.utils import timezone
from crm.models import Client


class Campagne(models.Model):
    """Campagne marketing"""
    TYPE_CAMPAGNE = [
        ('newsletter', 'Newsletter'),
        ('promotion', 'Promotion'),
        ('relance', 'Relance'),
        ('bienvenue', 'Bienvenue'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('planifiee', 'Planifiée'),
        ('active', 'Active'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    nom = models.CharField(max_length=200)
    type_campagne = models.CharField(max_length=20, choices=TYPE_CAMPAGNE, default='newsletter')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    
    description = models.TextField(blank=True)
    
    # Planification
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    
    # Segmentation
    segment = models.CharField(max_length=100, blank=True, help_text="Type de clients ciblés")
    
    # Contenu
    sujet = models.CharField(max_length=200)
    contenu_html = models.TextField()
    contenu_texte = models.TextField(blank=True)
    
    # Statistiques
    emails_envoyes = models.IntegerField(default=0)
    emails_ouverts = models.IntegerField(default=0)
    clics = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Campagne"
        verbose_name_plural = "Campagnes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nom} ({self.get_statut_display()})"
    
    @property
    def taux_ouverture(self):
        """Calcule le taux d'ouverture"""
        if self.emails_envoyes == 0:
            return 0
        return (self.emails_ouverts / self.emails_envoyes) * 100
    
    @property
    def taux_clic(self):
        """Calcule le taux de clic"""
        if self.emails_envoyes == 0:
            return 0
        return (self.clics / self.emails_envoyes) * 100
    
    @property
    def taux_conversion(self):
        """Calcule le taux de conversion"""
        if self.emails_envoyes == 0:
            return 0
        return (self.conversions / self.emails_envoyes) * 100


class EmailEnvoye(models.Model):
    """Emails envoyés individuels"""
    TYPE_EMAIL = [
        ('transactionnel', 'Transactionnel'),
        ('marketing', 'Marketing'),
        ('notification', 'Notification'),
    ]
    
    STATUT_EMAIL = [
        ('envoye', 'Envoyé'),
        ('ouvert', 'Ouvert'),
        ('clique', 'Cliqué'),
        ('erreur', 'Erreur'),
    ]
    
    campagne = models.ForeignKey(Campagne, on_delete=models.SET_NULL, null=True, blank=True, related_name='emails')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='emails_recus')
    
    type_email = models.CharField(max_length=20, choices=TYPE_EMAIL, default='marketing')
    statut = models.CharField(max_length=20, choices=STATUT_EMAIL, default='envoye')
    
    sujet = models.CharField(max_length=200)
    contenu = models.TextField()
    
    # Suivi
    date_envoi = models.DateTimeField(default=timezone.now)
    date_ouverture = models.DateTimeField(null=True, blank=True)
    date_clic = models.DateTimeField(null=True, blank=True)
    
    # Erreurs
    erreur = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Email envoyé"
        verbose_name_plural = "Emails envoyés"
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.sujet} → {self.client.email}"


class SequenceEmail(models.Model):
    """Séquence d'emails automatisés"""
    TYPE_SEQUENCE = [
        ('bienvenue', 'Bienvenue'),
        ('panier_abandonne', 'Panier abandonné'),
        ('nurturing', 'Nurturing'),
        ('reactivation', 'Réactivation'),
    ]
    
    nom = models.CharField(max_length=200)
    type_sequence = models.CharField(max_length=30, choices=TYPE_SEQUENCE)
    description = models.TextField(blank=True)
    
    actif = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Séquence email"
        verbose_name_plural = "Séquences email"
    
    def __str__(self):
        return self.nom


class EmailSequence(models.Model):
    """Email individuel dans une séquence"""
    sequence = models.ForeignKey(SequenceEmail, on_delete=models.CASCADE, related_name='emails')
    
    ordre = models.IntegerField(default=1)
    delai_jours = models.IntegerField(default=0, help_text="Nombre de jours après le déclencheur")
    
    sujet = models.CharField(max_length=200)
    contenu_html = models.TextField()
    contenu_texte = models.TextField(blank=True)
    
    actif = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Email de séquence"
        verbose_name_plural = "Emails de séquence"
        ordering = ['sequence', 'ordre']
    
    def __str__(self):
        return f"{self.sequence.nom} - Jour {self.delai_jours}"
