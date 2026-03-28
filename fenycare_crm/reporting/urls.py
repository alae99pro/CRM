"""
Reporting URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('ventes/', views.rapport_ventes, name='rapport_ventes'),
    path('clients/', views.rapport_clients, name='rapport_clients'),
    path('marketing/', views.rapport_marketing, name='rapport_marketing'),
    path('stock/', views.rapport_stock, name='rapport_stock'),
    path('export/', views.export_data, name='export_data'),
]
