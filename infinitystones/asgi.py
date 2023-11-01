"""
ASGI config for infinitystones project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels_auth_token_middlewares.middleware import HeaderAuthTokenMiddleware
from django.core.asgi import get_asgi_application

from infinitystones.routing import urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infinitystones.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket":
        AllowedHostsOriginValidator(
            HeaderAuthTokenMiddleware(
                URLRouter(urlpatterns)
            ),
        )
})
