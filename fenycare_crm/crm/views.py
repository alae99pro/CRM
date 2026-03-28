"""
CRM views - Gestion clients, prospects et interactions
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator

from .models import Client, Prospect, Interaction
from .forms import ClientForm, ProspectForm, InteractionForm


@login_required
def client_list(request):
    """Liste des clients avec filtres"""
    clients = Client.objects.all()
    
    # Filtres
    search = request.GET.get('search', '')
    type_client = request.GET.get('type', '')
    
    if search:
        clients = clients.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(email__icontains=search) |
            Q(entreprise__icontains=search)
        )
    
    if type_client:
        clients = clients.filter(type_client=type_client)
    
    # Pagination
    paginator = Paginator(clients, 20)
    page = request.GET.get('page', 1)
    clients_page = paginator.get_page(page)
    
    # Statistiques
    stats = {
        'total': Client.objects.count(),
        'particuliers': Client.objects.filter(type_client='particulier').count(),
        'professionnels': Client.objects.filter(type_client='professionnel').count(),
        'collectivites': Client.objects.filter(type_client='collectivite').count(),
    }
    
    context = {
        'clients': clients_page,
        'stats': stats,
        'search': search,
        'type_client': type_client,
    }
    return render(request, 'crm/client_list.html', context)


@login_required
def client_detail(request, pk):
    """Détail d'un client"""
    client = get_object_or_404(Client, pk=pk)
    interactions = client.interactions.all()[:10]
    commandes = client.commandes.all()[:10]
    
    context = {
        'client': client,
        'interactions': interactions,
        'commandes': commandes,
    }
    return render(request, 'crm/client_detail.html', context)


@login_required
def client_create(request):
    """Créer un nouveau client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, f'Client {client.get_full_name()} créé avec succès')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    
    return render(request, 'crm/client_form.html', {'form': form, 'action': 'Créer'})


@login_required
def client_edit(request, pk):
    """Modifier un client"""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client mis à jour avec succès')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'crm/client_form.html', {'form': form, 'action': 'Modifier', 'client': client})


@login_required
def prospect_list(request):
    """Liste des prospects avec pipeline"""
    prospects = Prospect.objects.select_related('responsable', 'converti_en_client')
    
    # Filtres
    statut = request.GET.get('statut', '')
    search = request.GET.get('search', '')
    
    if statut:
        prospects = prospects.filter(statut=statut)
    
    if search:
        prospects = prospects.filter(
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(email__icontains=search) |
            Q(entreprise__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(prospects, 20)
    page = request.GET.get('page', 1)
    prospects_page = paginator.get_page(page)
    
    # Statistiques pipeline
    stats = {
        'total': Prospect.objects.count(),
        'prospects': Prospect.objects.filter(statut='prospect').count(),
        'en_cours': Prospect.objects.filter(statut='en_cours').count(),
        'gagnes': Prospect.objects.filter(statut='gagne').count(),
        'perdus': Prospect.objects.filter(statut='perdu').count(),
        'valeur_pipeline': Prospect.objects.filter(
            statut__in=['prospect', 'en_cours']
        ).aggregate(Sum('montant_estime'))['montant_estime__sum'] or 0,
    }
    
    context = {
        'prospects': prospects_page,
        'stats': stats,
        'statut': statut,
        'search': search,
    }
    return render(request, 'crm/prospect_list.html', context)


@login_required
def prospect_detail(request, pk):
    """Détail d'un prospect"""
    prospect = get_object_or_404(Prospect, pk=pk)
    interactions = prospect.interactions.all()[:10]
    
    context = {
        'prospect': prospect,
        'interactions': interactions,
    }
    return render(request, 'crm/prospect_detail.html', context)


@login_required
def prospect_create(request):
    """Créer un nouveau prospect"""
    if request.method == 'POST':
        form = ProspectForm(request.POST)
        if form.is_valid():
            prospect = form.save()
            messages.success(request, f'Prospect {prospect.get_full_name()} créé avec succès')
            return redirect('prospect_detail', pk=prospect.pk)
    else:
        form = ProspectForm()
    
    return render(request, 'crm/prospect_form.html', {'form': form, 'action': 'Créer'})


@login_required
def prospect_edit(request, pk):
    """Modifier un prospect"""
    prospect = get_object_or_404(Prospect, pk=pk)
    
    if request.method == 'POST':
        form = ProspectForm(request.POST, instance=prospect)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prospect mis à jour avec succès')
            return redirect('prospect_detail', pk=prospect.pk)
    else:
        form = ProspectForm(instance=prospect)
    
    return render(request, 'crm/prospect_form.html', {'form': form, 'action': 'Modifier', 'prospect': prospect})


@login_required
def prospect_convert(request, pk):
    """Convertir un prospect en client"""
    prospect = get_object_or_404(Prospect, pk=pk)
    
    if prospect.converti_en_client:
        messages.warning(request, 'Ce prospect a déjà été converti en client')
        return redirect('prospect_detail', pk=pk)
    
    if request.method == 'POST':
        client = prospect.convertir_en_client(user=request.user)
        messages.success(request, f'Prospect converti en client avec succès : {client.get_full_name()}')
        return redirect('client_detail', pk=client.pk)
    
    return render(request, 'crm/prospect_convert.html', {'prospect': prospect})


@login_required
def interaction_create(request, client_pk=None, prospect_pk=None):
    """Créer une nouvelle interaction"""
    client = None
    prospect = None
    
    if client_pk:
        client = get_object_or_404(Client, pk=client_pk)
    elif prospect_pk:
        prospect = get_object_or_404(Prospect, pk=prospect_pk)
    
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.utilisateur = request.user
            if client:
                interaction.client = client
            elif prospect:
                interaction.prospect = prospect
            interaction.save()
            
            messages.success(request, 'Interaction enregistrée avec succès')
            
            if client:
                return redirect('client_detail', pk=client.pk)
            else:
                return redirect('prospect_detail', pk=prospect.pk)
    else:
        form = InteractionForm()
    
    context = {
        'form': form,
        'client': client,
        'prospect': prospect,
    }
    return render(request, 'crm/interaction_form.html', context)
