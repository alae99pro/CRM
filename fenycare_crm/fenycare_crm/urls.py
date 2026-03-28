"""
URL configuration for fenycare_crm project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('crm/', include('crm.urls')),
    path('marketing/', include('marketing.urls')),
    path('supply-chain/', include('supply_chain.urls')),
    path('reporting/', include('reporting.urls')),
    path('api/', include('fenycare_crm.api_urls')),
    
]

# Personnalisation de l'admin
admin.site.site_header = "FenyCare CRM Administration"
admin.site.site_title = "FenyCare CRM"
admin.site.index_title = "Tableau de bord administrateur"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
