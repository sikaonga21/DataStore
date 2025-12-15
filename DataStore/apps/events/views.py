from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from apps.projects.models import Project
from django.contrib.auth.decorators import login_required

@login_required
def event_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        
        Event.objects.create(
            project=project,
            title=title,
            description=description,
            date=date if date else None
        )
        return redirect('project_detail', pk=project_id)
    return render(request, 'events/form.html', {'project': project})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/detail.html', {'event': event})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        date = request.POST.get("date")
        
        event.date = date if date else None
        event.save()
        return redirect('event_detail', pk=pk)
    return render(request, 'events/form.html', {'event': event, 'project': event.project})
