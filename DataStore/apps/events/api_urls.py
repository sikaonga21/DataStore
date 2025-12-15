from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.EventListAPI.as_view(), name='api_event_list'),
    path('<int:pk>/', api_views.EventDetailAPI.as_view(), name='api_event_detail'),
]
