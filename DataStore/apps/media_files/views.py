from django.shortcuts import render, redirect, get_object_or_404
from .models import MediaFile
from apps.events.models import Event
from django.contrib.auth.decorators import login_required

@login_required
def media_upload(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            MediaFile.objects.create(event=event, file=file)
            return redirect('event_detail', pk=event_id)
    return render(request, 'media_files/form.html', {'event': event})
