import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Project
from apps.organizations.models import Organization

@method_decorator(csrf_exempt, name='dispatch')
class ProjectListAPI(View):
    def get(self, request):
        projects = Project.objects.all()
        
        status = request.GET.get('status')
        org_id = request.GET.get('organization')
        
        if status:
            projects = projects.filter(status=status)
        if org_id:
            projects = projects.filter(organization__id=org_id)
            
        data = []
        for p in projects:
            data.append({
                'id': p.id,
                'name': p.name,
                'organization_id': p.organization.id,
                'organization_name': p.organization.name,
                'status': p.status,
                'description': p.description,
            })
        return JsonResponse({'projects': data}, safe=False)

    def post(self, request):
        try:
            body = json.loads(request.body)
            org_id = body.get('organization_id')
            name = body.get('name')
            status = body.get('status', 'planned')
            
            if not org_id:
                return JsonResponse({'error': 'organization_id is required'}, status=400)
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            
            # Validate status
            valid_statuses = [c[0] for c in Project.STATUS_CHOICES]
            if status not in valid_statuses:
                 return JsonResponse({'error': f'Invalid status. Choices: {valid_statuses}'}, status=400)

            try:
                org = Organization.objects.get(pk=org_id)
            except Organization.DoesNotExist:
                return JsonResponse({'error': 'Invalid organization_id'}, status=400)

            project = Project.objects.create(
                organization=org,
                name=name,
                description=body.get('description', ''),
                status=status,
                start_date=body.get('start_date'),
                end_date=body.get('end_date')
            )
            return JsonResponse({'id': project.id, 'message': 'Project created'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ProjectDetailAPI(View):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            data = model_to_dict(project)
            # data['start_date'] = project.start_date.isoformat() if project.start_date else None
            # data['end_date'] = project.end_date.isoformat() if project.end_date else None
            return JsonResponse(data)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            body = json.loads(request.body)
            
            project.name = body.get('name', project.name)
            project.description = body.get('description', project.description)
            
            status = body.get('status')
            if status:
                valid_statuses = [c[0] for c in Project.STATUS_CHOICES]
                if status not in valid_statuses:
                    return JsonResponse({'error': f'Invalid status. Choices: {valid_statuses}'}, status=400)
                project.status = status
                
            project.save()
            return JsonResponse({'message': 'Project updated'})
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return JsonResponse({'message': 'Project deleted'})
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)
