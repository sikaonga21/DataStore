from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.ProjectListAPI.as_view(), name='api_project_list'),
    path('<int:pk>/', api_views.ProjectDetailAPI.as_view(), name='api_project_detail'),
]
