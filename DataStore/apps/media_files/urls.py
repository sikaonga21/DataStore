from django.urls import path
from . import views

urlpatterns = [
    path('upload/<int:event_id>/', views.media_upload, name='media_upload'),
]
