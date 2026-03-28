"""
CRM admin configuration
"""
from django.contrib import admin
from .models import Client, Prospect, Interaction


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'type_client', 'nombre_achats', 'montant_total_achats', 'created_at']
    list_filter = ['type_client', 'actif', 'created_at']
    search_fields = ['nom', 'prenom', 'email', 'entreprise', 'telephone']
    readonly_fields = ['created_at', 'updated_at', 'shopify_id']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'code_postal', 'pays')
        }),
        ('Informations commerciales', {
            'fields': ('type_client', 'entreprise', 'tags')
        }),
        ('Métriques', {
            'fields': ('date_premier_achat', 'nombre_achats', 'montant_total_achats')
        }),
        ('Shopify', {
            'fields': ('shopify_id',),
            'classes': ('collapse',)
        }),
        ('Autres', {
            'fields': ('notes', 'actif', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'statut', 'montant_estime', 'probabilite', 'responsable', 'created_at']
    list_filter = ['statut', 'source', 'created_at']
    search_fields = ['nom', 'prenom', 'email', 'entreprise']
    readonly_fields = ['created_at', 'updated_at', 'date_conversion']
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone', 'entreprise')
        }),
        ('Pipeline', {
            'fields': ('statut', 'source', 'montant_estime', 'probabilite', 'date_conversion_prevue', 'responsable')
        }),
        ('Conversion', {
            'fields': ('converti_en_client', 'date_conversion'),
            'classes': ('collapse',)
        }),
        ('Autres', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'type_interaction', 'client', 'prospect', 'utilisateur', 'date_interaction']
    list_filter = ['type_interaction', 'date_interaction']
    search_fields = ['sujet', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'date_interaction'
