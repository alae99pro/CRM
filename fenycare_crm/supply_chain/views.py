"""
Supply Chain views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator

from .models import Produit, Commande, LigneCommande, AlerteStock
from .forms import ProduitForm, CommandeForm


@login_required
def produit_list(request):
    """Liste des produits"""
    produits = Produit.objects.all()
    
    # Filtres
    search = request.GET.get('search', '')
    stock_bas = request.GET.get('stock_bas', '')
    
    if search:
        produits = produits.filter(
            Q(nom__icontains=search) |
            Q(reference__icontains=search) |
            Q(description__icontains=search)
        )
    
    if stock_bas:
        produits = [p for p in produits if p.stock_bas]
    
    # Pagination
    paginator = Paginator(produits, 20)
    page = request.GET.get('page', 1)
    produits_page = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total': Produit.objects.count(),
        'actifs': Produit.objects.filter(actif=True).count(),
        'stock_bas': len([p for p in Produit.objects.all() if p.stock_bas]),
        'valeur_totale': sum([p.valeur_stock for p in Produit.objects.all()]),
    }
    
    context = {
        'produits': produits_page,
        'stats': stats,
        'search': search,
        'stock_bas_filter': stock_bas,
    }
    return render(request, 'supply_chain/produit_list.html', context)


@login_required
def produit_detail(request, pk):
    """Détail d'un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    
    # Historique des commandes
    lignes_commande = LigneCommande.objects.filter(produit=produit).select_related('commande')[:20]
    
    context = {
        'produit': produit,
        'lignes_commande': lignes_commande,
    }
    return render(request, 'supply_chain/produit_detail.html', context)


@login_required
def produit_create(request):
    """Créer un nouveau produit"""
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save()
            messages.success(request, f'Produit {produit.nom} créé avec succès')
            return redirect('produit_detail', pk=produit.pk)
    else:
        form = ProduitForm()
    
    return render(request, 'supply_chain/produit_form.html', {'form': form, 'action': 'Créer'})


@login_required
def produit_edit(request, pk):
    """Modifier un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit mis à jour avec succès')
            return redirect('produit_detail', pk=produit.pk)
    else:
        form = ProduitForm(instance=produit)
    
    return render(request, 'supply_chain/produit_form.html', {'form': form, 'action': 'Modifier', 'produit': produit})


@login_required
def commande_list(request):
    """Liste des commandes"""
    commandes = Commande.objects.select_related('client')
    
    # Filtres
    statut = request.GET.get('statut', '')
    search = request.GET.get('search', '')
    
    if statut:
        commandes = commandes.filter(statut=statut)
    
    if search:
        commandes = commandes.filter(
            Q(numero_commande__icontains=search) |
            Q(client__nom__icontains=search) |
            Q(client__email__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(commandes, 20)
    page = request.GET.get('page', 1)
    commandes_page = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total': Commande.objects.count(),
        'en_attente': Commande.objects.filter(statut='en_attente').count(),
        'en_preparation': Commande.objects.filter(statut='en_preparation').count(),
        'expediees': Commande.objects.filter(statut='expediee').count(),
        'livrees': Commande.objects.filter(statut='livree').count(),
        'ca_total': Commande.objects.filter(statut='livree').aggregate(
            Sum('montant_total')
        )['montant_total__sum'] or 0,
    }
    
    context = {
        'commandes': commandes_page,
        'stats': stats,
        'statut': statut,
        'search': search,
    }
    return render(request, 'supply_chain/commande_list.html', context)


@login_required
def commande_detail(request, pk):
    """Détail d'une commande"""
    commande = get_object_or_404(Commande, pk=pk)
    lignes = commande.lignes.select_related('produit')
    
    context = {
        'commande': commande,
        'lignes': lignes,
    }
    return render(request, 'supply_chain/commande_detail.html', context)


@login_required
def alerte_stock_list(request):
    """Liste des alertes de stock"""
    alertes = AlerteStock.objects.filter(resolu=False).select_related('produit')
    
    context = {
        'alertes': alertes,
    }
    return render(request, 'supply_chain/alerte_stock_list.html', context)
