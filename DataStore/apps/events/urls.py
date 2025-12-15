from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:project_id>/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/update/', views.event_update, name='event_update'),
]
