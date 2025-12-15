from django.db import models

# Create your models here.
from django.db import models
from apps.events.models import Event

def upload_to(instance, filename):
    return f'project_media/{instance.event.project.id}/{filename}'

class MediaFile(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="media_files")
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
