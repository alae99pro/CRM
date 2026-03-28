"""
Marketing views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Campagne, EmailEnvoye, SequenceEmail
from .forms import CampagneForm


@login_required
def campagne_list(request):
    """Liste des campagnes marketing"""
    campagnes = Campagne.objects.all()
    
    # Filtres
    statut = request.GET.get('statut', '')
    search = request.GET.get('search', '')
    
    if statut:
        campagnes = campagnes.filter(statut=statut)
    
    if search:
        campagnes = campagnes.filter(
            Q(nom__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(campagnes, 15)
    page = request.GET.get('page', 1)
    campagnes_page = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total': Campagne.objects.count(),
        'actives': Campagne.objects.filter(statut='active').count(),
        'planifiees': Campagne.objects.filter(statut='planifiee').count(),
        'terminees': Campagne.objects.filter(statut='terminee').count(),
    }
    
    context = {
        'campagnes': campagnes_page,
        'stats': stats,
        'statut': statut,
        'search': search,
    }
    return render(request, 'marketing/campagne_list.html', context)


@login_required
def campagne_detail(request, pk):
    """Détail d'une campagne"""
    campagne = get_object_or_404(Campagne, pk=pk)
    emails = campagne.emails.all()[:50]
    
    context = {
        'campagne': campagne,
        'emails': emails,
    }
    return render(request, 'marketing/campagne_detail.html', context)


@login_required
def campagne_create(request):
    """Créer une nouvelle campagne"""
    if request.method == 'POST':
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne = form.save()
            messages.success(request, f'Campagne {campagne.nom} créée avec succès')
            return redirect('campagne_detail', pk=campagne.pk)
    else:
        form = CampagneForm()
    
    return render(request, 'marketing/campagne_form.html', {'form': form, 'action': 'Créer'})


@login_required
def campagne_edit(request, pk):
    """Modifier une campagne"""
    campagne = get_object_or_404(Campagne, pk=pk)
    
    if request.method == 'POST':
        form = CampagneForm(request.POST, instance=campagne)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campagne mise à jour avec succès')
            return redirect('campagne_detail', pk=campagne.pk)
    else:
        form = CampagneForm(instance=campagne)
    
    return render(request, 'marketing/campagne_form.html', {'form': form, 'action': 'Modifier', 'campagne': campagne})


@login_required
def email_list(request):
    """Liste des emails envoyés"""
    emails = EmailEnvoye.objects.select_related('client', 'campagne')
    
    # Filtres
    statut = request.GET.get('statut', '')
    campagne_id = request.GET.get('campagne', '')
    
    if statut:
        emails = emails.filter(statut=statut)
    
    if campagne_id:
        emails = emails.filter(campagne_id=campagne_id)
    
    # Pagination
    paginator = Paginator(emails, 30)
    page = request.GET.get('page', 1)
    emails_page = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total': EmailEnvoye.objects.count(),
        'envoyes': EmailEnvoye.objects.filter(statut='envoye').count(),
        'ouverts': EmailEnvoye.objects.filter(statut='ouvert').count(),
        'cliques': EmailEnvoye.objects.filter(statut='clique').count(),
        'erreurs': EmailEnvoye.objects.filter(statut='erreur').count(),
    }
    
    context = {
        'emails': emails_page,
        'stats': stats,
        'statut': statut,
        'campagnes': Campagne.objects.all(),
    }
    return render(request, 'marketing/email_list.html', context)


@login_required
def sequence_list(request):
    """Liste des séquences d'emails"""
    sequences = SequenceEmail.objects.prefetch_related('emails')
    
    context = {
        'sequences': sequences,
    }
    return render(request, 'marketing/sequence_list.html', context)


@login_required
def sequence_detail(request, pk):
    """Détail d'une séquence"""
    sequence = get_object_or_404(SequenceEmail, pk=pk)
    emails = sequence.emails.all()
    
    context = {
        'sequence': sequence,
        'emails': emails,
    }
    return render(request, 'marketing/sequence_detail.html', context)
