"""
Marketing forms
"""
from django import forms
from .models import Campagne


class CampagneForm(forms.ModelForm):
    class Meta:
        model = Campagne
        fields = [
            'nom', 'type_campagne', 'statut', 'description',
            'date_envoi', 'date_fin', 'segment',
            'sujet', 'contenu_html', 'contenu_texte'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type_campagne': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_envoi': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'date_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'segment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'particuliers, professionnels...'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu_html': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'contenu_texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }
