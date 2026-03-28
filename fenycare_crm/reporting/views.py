"""
Reporting views - Rapports et analyses
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
import json
import csv
from django.http import HttpResponse
from crm.models import Client, Prospect
from supply_chain.models import Commande, Produit
from marketing.models import Campagne, EmailEnvoye


@login_required
def rapport_ventes(request):
    """Rapport des ventes"""
    # Période
    periode = request.GET.get('periode', '30')  # 7, 30, 90, 365 jours
    jours = int(periode)
    date_debut = timezone.now() - timedelta(days=jours)
    
    # Commandes de la période
    commandes = Commande.objects.filter(date_commande__gte=date_debut)
    
    # Statistiques générales
    stats = {
        'total_commandes': commandes.filter(statut='livree').count(),
        'ca_total': commandes.filter(statut='livree').aggregate(
            Sum('montant_total')
        )['montant_total__sum'] or 0,
        'panier_moyen': commandes.filter(statut='livree').aggregate(
            Avg('montant_total')
        )['montant_total__avg'] or 0,
        'commandes_en_cours': commandes.exclude(statut__in=['livree', 'annulee']).count(),
    }
    
    # Ventes par jour (pour le graphique)
    from django.db.models.functions import TruncDate
    ventes_par_jour = commandes.filter(statut='livree').annotate(
        jour=TruncDate('date_commande')
    ).values('jour').annotate(
        ca=Sum('montant_total'),
        nb_commandes=Count('id')
    ).order_by('jour')
    
    # Top produits
    from supply_chain.models import LigneCommande
    top_produits = LigneCommande.objects.filter(
        commande__date_commande__gte=date_debut,
        commande__statut='livree'
    ).values(
        'produit__nom'
    ).annotate(
        quantite_vendue=Sum('quantite'),
        ca=Sum('prix_total')
    ).order_by('-ca')[:10]
    
    # Ventes par type de client
    ventes_par_type = commandes.filter(statut='livree').values(
        'client__type_client'
    ).annotate(
        ca=Sum('montant_total'),
        nb_commandes=Count('id')
    )
    
    context = {
        'stats': stats,
        'ventes_par_jour': list(ventes_par_jour),
        'top_produits': top_produits,
        'ventes_par_type': ventes_par_type,
        'periode': periode,
    }
    return render(request, 'reporting/rapport_ventes.html', context)


@login_required
def rapport_clients(request):
    """Rapport clients"""
    # Période
    periode = request.GET.get('periode', '30')
    jours = int(periode)
    date_debut = timezone.now() - timedelta(days=jours)
    
    # Statistiques clients
    stats = {
        'total_clients': Client.objects.count(),
        'nouveaux_clients': Client.objects.filter(created_at__gte=date_debut).count(),
        'clients_actifs': Client.objects.filter(actif=True).count(),
        'total_prospects': Prospect.objects.count(),
        'prospects_actifs': Prospect.objects.filter(statut__in=['prospect', 'en_cours']).count(),
    }
    
    # Répartition par type
    clients_par_type = Client.objects.values('type_client').annotate(
        count=Count('id')
    )
    
    # Top clients (par CA)
    top_clients = Client.objects.filter(
        commandes__statut='livree',
        commandes__date_commande__gte=date_debut
    ).annotate(
        ca=Sum('commandes__montant_total')
    ).order_by('-ca')[:10]
    
    # Conversion prospects
    prospects_stats = {
        'prospect': Prospect.objects.filter(statut='prospect').count(),
        'en_cours': Prospect.objects.filter(statut='en_cours').count(),
        'gagne': Prospect.objects.filter(statut='gagne').count(),
        'perdu': Prospect.objects.filter(statut='perdu').count(),
    }
    total_prospects = sum(prospects_stats.values())
    taux_conversion = (prospects_stats['gagne'] / total_prospects * 100) if total_prospects > 0 else 0
    
    context = {
        'stats': stats,
        'clients_par_type': clients_par_type,
        'top_clients': top_clients,
        'prospects_stats': prospects_stats,
        'taux_conversion': round(taux_conversion, 2),
        'periode': periode,
    }
    return render(request, 'reporting/rapport_clients.html', context)


@login_required
def rapport_marketing(request):
    """Rapport marketing"""
    # Période
    periode = request.GET.get('periode', '30')
    jours = int(periode)
    date_debut = timezone.now() - timedelta(days=jours)
    
    # Campagnes de la période
    campagnes = Campagne.objects.filter(created_at__gte=date_debut)
    
    # Statistiques générales
    total_emails = EmailEnvoye.objects.filter(date_envoi__gte=date_debut).count()
    emails_ouverts = EmailEnvoye.objects.filter(
        date_envoi__gte=date_debut,
        statut__in=['ouvert', 'clique']
    ).count()
    emails_cliques = EmailEnvoye.objects.filter(
        date_envoi__gte=date_debut,
        statut='clique'
    ).count()
    
    taux_ouverture_global = (emails_ouverts / total_emails * 100) if total_emails > 0 else 0
    taux_clic_global = (emails_cliques / total_emails * 100) if total_emails > 0 else 0
    
    stats = {
        'total_campagnes': campagnes.count(),
        'campagnes_actives': campagnes.filter(statut='active').count(),
        'total_emails': total_emails,
        'taux_ouverture': round(taux_ouverture_global, 2),
        'taux_clic': round(taux_clic_global, 2),
    }
    
    # Performance par campagne
    campagnes_perf = campagnes.filter(emails_envoyes__gt=0).order_by('-created_at')[:10]
    
    # Emails par jour
    from django.db.models.functions import TruncDate
    emails_par_jour = EmailEnvoye.objects.filter(
        date_envoi__gte=date_debut
    ).annotate(
        jour=TruncDate('date_envoi')
    ).values('jour').annotate(
        envoyes=Count('id'),
        ouverts=Count('id', filter=Q(statut__in=['ouvert', 'clique']))
    ).order_by('jour')
    
    context = {
        'stats': stats,
        'campagnes_perf': campagnes_perf,
        'emails_par_jour': list(emails_par_jour),
        'periode': periode,
    }
    return render(request, 'reporting/rapport_marketing.html', context)


@login_required
def rapport_stock(request):
    """Rapport stock"""
    # Tous les produits
    produits = Produit.objects.all()
    
    # Produits en stock bas
    produits_stock_bas = [p for p in produits if p.stock_bas]
    
    # Statistiques
    stats = {
        'total_produits': produits.count(),
        'produits_actifs': produits.filter(actif=True).count(),
        'produits_stock_bas': len(produits_stock_bas),
        'valeur_totale_stock': sum([p.valeur_stock for p in produits]),
    }
    
    # Produits les plus vendus
    from supply_chain.models import LigneCommande
    from datetime import timedelta
    date_debut = timezone.now() - timedelta(days=90)
    
    produits_vendus = LigneCommande.objects.filter(
        commande__date_commande__gte=date_debut
    ).values('produit__nom', 'produit__quantite_stock').annotate(
        quantite_vendue=Sum('quantite')
    ).order_by('-quantite_vendue')[:10]
    
    context = {
        'stats': stats,
        'produits_stock_bas': produits_stock_bas[:20],
        'produits_vendus': produits_vendus,
    }
    return render(request, 'reporting/rapport_stock.html', context)


@login_required
def export_data(request):
    """Page d'export de données et génération de CSV"""
    type_export = request.GET.get('type')
    
    # Si pas de type défini, on affiche juste la page
    if not type_export:
        return render(request, 'reporting/export_data.html')
        
    periode = request.GET.get('periode', '30')
    
    # Préparation de la réponse HTTP pour le téléchargement CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    prefix = f"export_{type_export}_{timezone.now().strftime('%Y%m%d_%H%M')}"
    response['Content-Disposition'] = f'attachment; filename="{prefix}.csv"'
    
    # BOM pour que Excel reconnaisse l'UTF-8 directement
    response.write('\ufeff'.encode('utf8'))
    
    writer = csv.writer(response, delimiter=';')
    
    # Gestion des périodes
    jours = None
    if periode != 'all':
        try:
            jours = int(periode)
        except ValueError:
            jours = 30
            
    date_debut = timezone.now() - timedelta(days=jours) if jours else None
    
    # --- EXPORT VENTES (Commandes) ---
    if type_export == 'ventes':
        commandes = Commande.objects.select_related('client').all()
        if date_debut:
            commandes = commandes.filter(date_commande__gte=date_debut)
            
        writer.writerow([
            'Numéro', 'Date', 'Client', 'Statut', 
            'Montant Produits', 'Frais Livraison', 'Montant Total', 
            'Ville', 'Pays'
        ])
        for c in commandes:
            writer.writerow([
                c.numero_commande,
                c.date_commande.strftime('%Y-%m-%d %H:%M'),
                c.client.get_full_name(),
                c.get_statut_display(),
                c.montant_produits,
                c.frais_livraison,
                c.montant_total,
                c.ville_livraison,
                c.pays_livraison
            ])
            
    # --- EXPORT CLIENTS ---
    elif type_export == 'clients':
        clients = Client.objects.all()
        if date_debut:
            clients = clients.filter(created_at__gte=date_debut)
            
        # Agrégation du CA total par client
        clients = clients.annotate(total_depense=Sum('commandes__montant_total'))
            
        writer.writerow([
            'Nom', 'Prénom', 'Email', 'Téléphone', 
            'Type', 'Entreprise', 'Date Inscription', 'CA Total'
        ])
        for c in clients:
            writer.writerow([
                c.nom,
                c.prenom,
                c.email,
                c.telephone,
                c.get_type_client_display(),
                c.entreprise,
                c.created_at.strftime('%Y-%m-%d'),
                c.total_depense or 0
            ])
            
    # --- EXPORT MARKETING (Campagnes) ---
    elif type_export == 'marketing':
        campagnes = Campagne.objects.all()
        if date_debut:
            campagnes = campagnes.filter(created_at__gte=date_debut)
            
        writer.writerow([
            'Nom', 'Type', 'Statut', 'Créée le', 
            'Emails Envoyés', 'Ouverts', 'Clics', 'Conversions', 
            'Taux Ouverture (%)', 'Taux Clic (%)'
        ])
        for c in campagnes:
            writer.writerow([
                c.nom,
                c.get_type_campagne_display(),
                c.get_statut_display(),
                c.created_at.strftime('%Y-%m-%d'),
                c.emails_envoyes,
                c.emails_ouverts,
                c.clics,
                c.conversions,
                round(c.taux_ouverture, 2),
                round(c.taux_clic, 2)
            ])
            
    # --- EXPORT STOCK (Produits) ---
    elif type_export == 'stock':
        produits = Produit.objects.all()
        
        writer.writerow([
            'Référence', 'Nom', 'Prix Unitaire', 'Quantité en Stock', 
            'Seuil Alerte', 'Statut', 'Stock Bas', 'Valeur Totale'
        ])
        for p in produits:
            writer.writerow([
                p.reference,
                p.nom,
                p.prix_unitaire,
                p.quantite_stock,
                p.seuil_alerte,
                'Actif' if p.actif else 'Inactif',
                'Oui' if p.stock_bas else 'Non',
                p.valeur_stock
            ])
            
    return response
