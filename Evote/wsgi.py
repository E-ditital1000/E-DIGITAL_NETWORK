"""
WSGI config for Evote project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Evote.settings')

application = get_wsgi_application()
import os
import sys

path = 'C:/Users/ELVIS/Desktop/project/Evote/Evote'  # Path to your Django project's root directory
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Evote.settings'  # Replace 'your_project' with your actual project name

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
