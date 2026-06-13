"""
WSGI config for commitclub project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commitclub.settings')

application = get_wsgi_application()
