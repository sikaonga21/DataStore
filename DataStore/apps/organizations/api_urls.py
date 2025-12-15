from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.OrganizationListAPI.as_view(), name='api_organization_list'),
    path('<int:pk>/', api_views.OrganizationDetailAPI.as_view(), name='api_organization_detail'),
]
