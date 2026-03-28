"""
API URLs configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Les ViewSets seront ajoutés ici au fur et à mesure
# Exemple: router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
