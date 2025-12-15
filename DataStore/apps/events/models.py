from django.db import models

# Create your models here.
from django.db import models
from apps.projects.models import Project

class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
