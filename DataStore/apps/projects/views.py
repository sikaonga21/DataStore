from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Project
from apps.organizations.models import Organization


@login_required
def project_list(request):
    projects_qs = Project.objects.select_related("organization").all()

    # Get filters from query params
    status = request.GET.get("status", "")
    org_id = request.GET.get("organization", "")

    # Apply filters
    if status:
        projects_qs = projects_qs.filter(status=status)

    if org_id:
        projects_qs = projects_qs.filter(organization_id=org_id)

    # Pagination
    paginator = Paginator(projects_qs, 10)
    page_number = request.GET.get("page")
    projects = paginator.get_page(page_number)

    # For filter dropdown
    organizations = Organization.objects.all()

    context = {
        "projects": projects,
        "organizations": organizations,
        "current_status": status,   # string (e.g. "ongoing")
        "current_org": org_id,       # string (e.g. "3")
    }

    return render(request, "projects/list.html", context)


@login_required
def project_create(request, org_id):
    organization = get_object_or_404(Organization, pk=org_id)

    if request.method == "POST":
        Project.objects.create(
            organization=organization,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            start_date=request.POST.get("start_date") or None,
            end_date=request.POST.get("end_date") or None,
        )
        return redirect("organization_detail", pk=org_id)

    return render(request, "projects/form.html", {
        "organization": organization
    })


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/detail.html", {
        "project": project
    })


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        project.name = request.POST.get("name")
        project.description = request.POST.get("description")
        project.start_date = request.POST.get("start_date") or None
        project.end_date = request.POST.get("end_date") or None
        project.save()

        return redirect("project_detail", pk=pk)

    return render(request, "projects/form.html", {
        "project": project,
        "organization": project.organization,
    })
