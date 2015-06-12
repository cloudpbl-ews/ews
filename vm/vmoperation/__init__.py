from django.conf import settings
if settings.PRODUCTION:
    from .production import *
else:
    from .dev import *
