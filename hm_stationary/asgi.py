"""
ASGI config for hm_stationary project.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from stationary_system import routing as stationary_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hm_stationary.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
'http': django_asgi_app,
'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(stationary_routing.websocket_urlpatterns)
    )
),
})
