# home/routing.py
from django.urls import re_path
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('stream', consumers.VideoStreamConsumer.as_asgi()),
]