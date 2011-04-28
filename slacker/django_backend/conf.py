from django.conf import settings
SLACKER_SERVER = getattr(settings, 'SLACKER_SERVER', 'http://127.0.0.1:8000')
