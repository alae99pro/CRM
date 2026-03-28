"""
CRM URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
    
    # Prospects
    path('prospects/', views.prospect_list, name='prospect_list'),
    path('prospects/create/', views.prospect_create, name='prospect_create'),
    path('prospects/<int:pk>/', views.prospect_detail, name='prospect_detail'),
    path('prospects/<int:pk>/edit/', views.prospect_edit, name='prospect_edit'),
    path('prospects/<int:pk>/convert/', views.prospect_convert, name='prospect_convert'),
    
    # Interactions
    path('interactions/create/client/<int:client_pk>/', views.interaction_create, name='interaction_create_client'),
    path('interactions/create/prospect/<int:prospect_pk>/', views.interaction_create, name='interaction_create_prospect'),
]
