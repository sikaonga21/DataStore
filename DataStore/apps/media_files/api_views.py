import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import MediaFile
from apps.events.models import Event

@method_decorator(csrf_exempt, name='dispatch')
class MediaListAPI(View):
    def get(self, request):
        event_id = request.GET.get('event')
        media_files = MediaFile.objects.all()
        
        if event_id:
            media_files = media_files.filter(event__id=event_id)
            
        data = []
        for m in media_files:
            data.append({
                'id': m.id,
                'event_id': m.event.id,
                'file_url': m.file.url,
                'uploaded_at': m.uploaded_at.isoformat(),
            })
        return JsonResponse({'media_files': data}, safe=False)

    def post(self, request):
        # Multipart form data handling
        event_id = request.POST.get('event_id')
        file = request.FILES.get('file')
        
        if not event_id or not file:
            return JsonResponse({'error': 'event_id and file are required'}, status=400)
            
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Invalid event_id'}, status=400)
            
        media = MediaFile.objects.create(event=event, file=file)
        return JsonResponse({'id': media.id, 'file_url': media.file.url, 'message': 'File uploaded'}, status=201)
