
import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
sys.path.append('/var/www/stock')
sys.path.append('/var/www')
application = get_wsgi_application()
