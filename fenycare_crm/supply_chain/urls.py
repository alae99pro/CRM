"""
Supply Chain URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    # Produits
    path('produits/', views.produit_list, name='produit_list'),
    path('produits/create/', views.produit_create, name='produit_create'),
    path('produits/<int:pk>/', views.produit_detail, name='produit_detail'),
    path('produits/<int:pk>/edit/', views.produit_edit, name='produit_edit'),
    
    # Commandes
    path('commandes/', views.commande_list, name='commande_list'),
    path('commandes/<int:pk>/', views.commande_detail, name='commande_detail'),
    
    # Alertes stock
    path('alertes-stock/', views.alerte_stock_list, name='alerte_stock_list'),
]
