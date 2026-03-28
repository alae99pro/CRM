"""
Core views - Dashboard and authentication
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import timedelta

from crm.models import Client, Prospect
from supply_chain.models import Commande, Produit
from marketing.models import Campagne


def login_view(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.get_full_name() or user.username} !')
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants incorrects')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté')
    return redirect('login')


@login_required
def dashboard(request):
    """Tableau de bord principal"""
    # Période d'analyse (30 derniers jours)
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    
    # Statistiques clients
    total_clients = Client.objects.count()
    new_clients_30d = Client.objects.count()
    total_prospects = Prospect.objects.count()
    prospects_en_cours = Prospect.objects.filter(statut='en_cours').count()
    
    # Statistiques commandes
    total_commandes = Commande.objects.count()
    commandes_30d = Commande.objects.count()
    ca_total = Commande.objects.filter(statut='livree').aggregate(
        total=Sum('montant_total')
    )['total'] or 0
    ca_30d = Commande.objects.filter(
        statut='livree',
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    # Commandes par statut
    commandes_par_statut = Commande.objects.values('statut').annotate(
        count=Count('id')
    )
    
    # Statistiques stock
    total_produits = Produit.objects.count()
    produits_stock_bas = Produit.objects.filter(
        quantite_stock__lte=F('seuil_alerte')
    ).count()
    
    # Statistiques marketing
    campagnes_actives = Campagne.objects.filter(statut='active').count()
    campagnes_30d = Campagne.objects.count()
    
    # Dernières activités
    dernieres_commandes = Commande.objects.select_related('client').order_by('-date_commande')[:5]
    derniers_prospects = Prospect.objects.order_by('-created_at')[:5]
    
    # Taux de conversion (prospects gagnés / total prospects)
    prospects_gagnes = Prospect.objects.filter(statut='gagne').count()
    taux_conversion = (prospects_gagnes / total_prospects * 100) if total_prospects > 0 else 0
    
    context = {
        'total_clients': total_clients,
        'new_clients_30d': new_clients_30d,
        'total_prospects': total_prospects,
        'prospects_en_cours': prospects_en_cours,
        'total_commandes': total_commandes,
        'commandes_30d': commandes_30d,
        'ca_total': ca_total,
        'ca_30d': ca_30d,
        'commandes_par_statut': commandes_par_statut,
        'total_produits': total_produits,
        'produits_stock_bas': produits_stock_bas,
        'campagnes_actives': campagnes_actives,
        'campagnes_30d': campagnes_30d,
        'dernieres_commandes': dernieres_commandes,
        'derniers_prospects': derniers_prospects,
        'taux_conversion': round(taux_conversion, 2),
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_view(request):
    """Page de profil utilisateur"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        profile = user.profile
        profile.phone = request.POST.get('phone', '')
        profile.save()
        
        messages.success(request, 'Profil mis à jour avec succès')
        return redirect('profile')
    
    return render(request, 'core/profile.html')
