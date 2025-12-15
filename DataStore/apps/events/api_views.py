import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Event
from apps.projects.models import Project

@method_decorator(csrf_exempt, name='dispatch')
class EventListAPI(View):
    def get(self, request):
        events = Event.objects.all()
        project_id = request.GET.get('project')
        
        if project_id:
            events = events.filter(project__id=project_id)
            
        data = []
        for e in events:
            data.append({
                'id': e.id,
                'title': e.title,
                'project_id': e.project.id,
                'project_name': e.project.name,
                'date': e.date,
                'description': e.description,
            })
        return JsonResponse({'events': data}, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            project_id = body.get('project_id')
            title = body.get('title')
            
            if not project_id:
                return JsonResponse({'error': 'project_id is required'}, status=400)
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)
            
            try:
                project = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Invalid project_id'}, status=400)

            event = Event.objects.create(
                project=project,
                title=title,
                description=body.get('description', ''),
                date=body.get('date'),
            )
            return JsonResponse({'id': event.id, 'message': 'Event created'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class EventDetailAPI(View):
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            data = model_to_dict(event)
            return JsonResponse(data)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return JsonResponse({'message': 'Event deleted'})
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
