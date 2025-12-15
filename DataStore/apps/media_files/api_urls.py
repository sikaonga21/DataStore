from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.MediaListAPI.as_view(), name='api_media_list'),
]
