"""
WSGI config for Uranus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from Uranus.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Uranus.settings")
sys.path.append(BASE_DIR)

application = get_wsgi_application()
