"""
Supply Chain admin configuration
"""
from django.contrib import admin
from .models import Produit, Commande, LigneCommande, AlerteStock


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1
    readonly_fields = ['prix_total']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'reference', 'prix_unitaire', 'quantite_stock', 'seuil_alerte', 'stock_bas', 'actif']
    list_filter = ['actif', 'created_at']
    search_fields = ['nom', 'reference', 'description']
    readonly_fields = ['created_at', 'updated_at', 'shopify_id']
    
    def stock_bas(self, obj):
        return obj.stock_bas
    stock_bas.boolean = True
    stock_bas.short_description = 'Stock bas'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['numero_commande', 'client', 'statut', 'montant_total', 'date_commande']
    list_filter = ['statut', 'date_commande']
    search_fields = ['numero_commande', 'client__nom', 'client__email']
    readonly_fields = ['created_at', 'updated_at', 'shopify_id', 'montant_total']
    date_hierarchy = 'date_commande'
    inlines = [LigneCommandeInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero_commande', 'client', 'statut', 'date_commande')
        }),
        ('Montants', {
            'fields': ('montant_produits', 'frais_livraison', 'montant_total')
        }),
        ('Livraison', {
            'fields': ('adresse_livraison', 'ville_livraison', 'code_postal_livraison', 'pays_livraison')
        }),
        ('Suivi', {
            'fields': ('numero_suivi', 'transporteur', 'date_expedition', 'date_livraison')
        }),
        ('Shopify', {
            'fields': ('shopify_id',),
            'classes': ('collapse',)
        }),
        ('Autres', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(AlerteStock)
class AlerteStockAdmin(admin.ModelAdmin):
    list_display = ['produit', 'quantite_actuelle', 'seuil', 'resolu', 'created_at']
    list_filter = ['resolu', 'created_at']
    search_fields = ['produit__nom']
    readonly_fields = ['created_at']
