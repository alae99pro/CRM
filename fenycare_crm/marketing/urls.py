"""
Marketing URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    # Campagnes
    path('campagnes/', views.campagne_list, name='campagne_list'),
    path('campagnes/create/', views.campagne_create, name='campagne_create'),
    path('campagnes/<int:pk>/', views.campagne_detail, name='campagne_detail'),
    path('campagnes/<int:pk>/edit/', views.campagne_edit, name='campagne_edit'),
    
    # Emails
    path('emails/', views.email_list, name='email_list'),
    
    # Séquences
    path('sequences/', views.sequence_list, name='sequence_list'),
    path('sequences/<int:pk>/', views.sequence_detail, name='sequence_detail'),
]
