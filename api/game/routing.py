from django.urls import re_path
from .consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_id>[0-9a-f-]+)/$', GameConsumer.as_asgi()),
]
