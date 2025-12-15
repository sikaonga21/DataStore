from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from apps.organizations.models import Organization
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

@login_required
def project_list(request):
    projects_list = Project.objects.all()
    
    # Filtering
    status = request.GET.get('status')
    org_id = request.GET.get('organization')
    
    if status:
        projects_list = projects_list.filter(status=status)
    if org_id:
        projects_list = projects_list.filter(organization__id=org_id)
        
    paginator = Paginator(projects_list, 10)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    organizations = Organization.objects.all() # For filter dropdown
    
    return render(request, 'projects/list.html', {
        'projects': projects, 
        'organizations': organizations,
        'current_status': status,
        'current_org': int(org_id) if org_id else None
    })

@login_required
def project_create(request, org_id):
    organization = get_object_or_404(Organization, pk=org_id)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        
        Project.objects.create(
            organization=organization,
            name=name,
            description=description,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None
        )
        return redirect('organization_detail', pk=org_id)
    return render(request, 'projects/form.html', {'organization': organization})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/detail.html', {'project': project})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        
        project.start_date = start_date if start_date else None
        project.end_date = end_date if end_date else None
        
        project.save()
        return redirect('project_detail', pk=pk)
    return render(request, 'projects/form.html', {'project': project, 'organization': project.organization})
