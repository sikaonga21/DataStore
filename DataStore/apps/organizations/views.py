from django.shortcuts import render, redirect, get_object_or_404
from .models import Organization
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def organization_list(request):
    query = request.GET.get('q', '')
    organizations_list = Organization.objects.all()
    
    if query:
        organizations_list = organizations_list.filter(name__icontains=query)
    
    paginator = Paginator(organizations_list, 10) # Show 10 organizations per page
    page_number = request.GET.get('page')
    organizations = paginator.get_page(page_number)
    
    return render(request, 'organizations/list.html', {'organizations': organizations, 'query': query})

@login_required
def organization_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        contact_email = request.POST.get("contact_email")
        
        Organization.objects.create(name=name, description=description, contact_email=contact_email)
        return redirect('organization_list')
    return render(request, 'organizations/form.html')

@login_required
def organization_detail(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/detail.html', {'organization': organization})

@login_required
def organization_update(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    if request.method == "POST":
        organization.name = request.POST.get("name")
        organization.description = request.POST.get("description")
        organization.contact_email = request.POST.get("contact_email")
        organization.save()
        return redirect('organization_detail', pk=pk)
    return render(request, 'organizations/form.html', {'organization': organization})
