"""
Supply Chain forms
"""
from django import forms
from .models import Produit, Commande


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'nom', 'description', 'reference',
            'prix_unitaire', 'prix_achat',
            'quantite_stock', 'seuil_alerte',
            'image', 'actif'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prix_achat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantite_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'seuil_alerte': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = [
            'numero_commande', 'client', 'statut',
            'montant_produits', 'frais_livraison',
            'adresse_livraison', 'ville_livraison', 'code_postal_livraison', 'pays_livraison',
            'numero_suivi', 'transporteur', 'notes'
        ]
        widgets = {
            'numero_commande': forms.TextInput(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'montant_produits': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'frais_livraison': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'adresse_livraison': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ville_livraison': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal_livraison': forms.TextInput(attrs={'class': 'form-control'}),
            'pays_livraison': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_suivi': forms.TextInput(attrs={'class': 'form-control'}),
            'transporteur': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
