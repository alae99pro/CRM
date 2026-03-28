"""
Marketing admin configuration
"""
from django.contrib import admin
from .models import Campagne, EmailEnvoye, SequenceEmail, EmailSequence


@admin.register(Campagne)
class CampagneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_campagne', 'statut', 'emails_envoyes', 'taux_ouverture', 'taux_clic', 'date_envoi']
    list_filter = ['statut', 'type_campagne', 'date_envoi']
    search_fields = ['nom', 'description', 'sujet']
    readonly_fields = ['created_at', 'updated_at', 'emails_envoyes', 'emails_ouverts', 'clics', 'conversions']
    
    def taux_ouverture(self, obj):
        return f"{obj.taux_ouverture:.2f}%"
    taux_ouverture.short_description = 'Taux ouverture'
    
    def taux_clic(self, obj):
        return f"{obj.taux_clic:.2f}%"
    taux_clic.short_description = 'Taux clic'


@admin.register(EmailEnvoye)
class EmailEnvoyeAdmin(admin.ModelAdmin):
    list_display = ['sujet', 'client', 'type_email', 'statut', 'date_envoi']
    list_filter = ['statut', 'type_email', 'date_envoi']
    search_fields = ['sujet', 'client__email', 'client__nom']
    readonly_fields = ['created_at']
    date_hierarchy = 'date_envoi'


class EmailSequenceInline(admin.TabularInline):
    model = EmailSequence
    extra = 1


@admin.register(SequenceEmail)
class SequenceEmailAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type_sequence', 'actif', 'created_at']
    list_filter = ['type_sequence', 'actif']
    search_fields = ['nom', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [EmailSequenceInline]
