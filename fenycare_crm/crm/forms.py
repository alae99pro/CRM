"""
CRM forms
"""
from django import forms
from .models import Client, Prospect, Interaction


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nom', 'prenom', 'email', 'telephone',
            'adresse', 'ville', 'code_postal', 'pays',
            'type_client', 'entreprise', 'tags', 'notes', 'actif'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'parent, premium, fidèle...'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProspectForm(forms.ModelForm):
    class Meta:
        model = Prospect
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'entreprise',
            'statut', 'source', 'montant_estime', 'probabilite',
            'date_conversion_prevue', 'responsable', 'notes'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'entreprise': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'montant_estime': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'probabilite': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'date_conversion_prevue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['type_interaction', 'sujet', 'description', 'date_interaction']
        widgets = {
            'type_interaction': forms.Select(attrs={'class': 'form-select'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_interaction': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
