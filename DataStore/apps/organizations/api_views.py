import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Organization

@method_decorator(csrf_exempt, name='dispatch')
class OrganizationListAPI(View):
    def get(self, request):
        name_filter = request.GET.get('name')
        organizations = Organization.objects.all()
        
        if name_filter:
            organizations = organizations.filter(name__icontains=name_filter)
            
        data = []
        for org in organizations:
            data.append({
                'id': org.id,
                'name': org.name,
                'description': org.description,
                'contact_email': org.contact_email,
                'created_at': org.created_at.isoformat(),
            })
            
        # Pagination could be added here similar to views, but simple list for now
        return JsonResponse({'organizations': data}, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            name = body.get('name')
            description = body.get('description', '')
            contact_email = body.get('contact_email', '')
            
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            
            if Organization.objects.filter(name=name).exists():
                 return JsonResponse({'error': 'Organization with this name already exists'}, status=400)
            
            org = Organization.objects.create(name=name, description=description, contact_email=contact_email)
            return JsonResponse({'id': org.id, 'message': 'Organization created'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class OrganizationDetailAPI(View):
    def get(self, request, pk):
        try:
            org = Organization.objects.get(pk=pk)
            data = model_to_dict(org)
            data['created_at'] = org.created_at.isoformat()
            return JsonResponse(data)
        except Organization.DoesNotExist:
            return JsonResponse({'error': 'Organization not found'}, status=404)

    def put(self, request, pk):
        try:
            org = Organization.objects.get(pk=pk)
            body = json.loads(request.body)
            
            org.name = body.get('name', org.name)
            org.description = body.get('description', org.description)
            org.contact_email = body.get('contact_email', org.contact_email)
            org.save()
            
            return JsonResponse({'message': 'Organization updated'})
        except Organization.DoesNotExist:
            return JsonResponse({'error': 'Organization not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    def delete(self, request, pk):
        try:
            org = Organization.objects.get(pk=pk)
            if org.projects.exists(): # Validate cascade / protection
                 # Requirement: Must cascade relationships (implied: handle properly). 
                 # Often explicit delete is preferred, or cascade. 
                 # Django defaults to CASCADE, but for API safety let's warn or allow.
                 # User instructions: "Must cascade relationships". Django on_delete=CASCADE handles this automatically.
                 pass 
            
            org.delete()
            return JsonResponse({'message': 'Organization deleted'})
        except Organization.DoesNotExist:
            return JsonResponse({'error': 'Organization not found'}, status=404)
