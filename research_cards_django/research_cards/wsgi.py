"""
WSGI config for research_cards project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import logging
logging.error("WSGI file loaded")
logging.error(os.listdir('.'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'research_cards.settings')

application = get_wsgi_application()
