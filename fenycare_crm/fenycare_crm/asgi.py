"""
ASGI config for fenycare_crm project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fenycare_crm.settings')

application = get_asgi_application()
