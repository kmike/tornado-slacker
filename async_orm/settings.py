from django.conf import settings
HTTP_SERVER = getattr(settings, 'ASYNC_ORM_HTTP_SERVER', 'http://127.0.0.1:8000')
