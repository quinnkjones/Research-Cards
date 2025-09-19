from django.shortcuts import render,HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from rest_framework import viewsets,permissions


from django.conf import settings

from rest_framework.decorators import api_view
from .models import Project, Hypothesis, Experiment, Result, User
import json
import random

'''

'''


# Create your views here.
def index(request):
    return HttpResponse("Hello, World")

@api_view(['GET'])
def project_list(request):
    api_key = request.headers.get('x-api-key')
    user = User.objects.filter(api_key=api_key).first()

    projects = Project.objects.filter(owner=user)

    json_data = {
        "projects": [{"id": p.id, "name": p.name, "description": p.description} for p in projects]
    }

    return HttpResponse("Project List - Total Projects: " + str(projects.count()) + "\n" + json.dumps(json_data, indent=2))

@api_view(['GET'])
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return HttpResponse(f"Project Detail: {project.name} {project.description}")

@api_view(['POST'])
def project_create(request):
    api_key = request.headers.get('x-api-key')
    user = User.objects.filter(api_key=api_key).first()

    if not user:
        return HttpResponse("Unauthorized", status=401)

    project = Project.objects.create(
        name=request.POST.get('name'),
        description=request.POST.get('description'),
        owner=user
    )
    project.save()
    return HttpResponse("Project Create")

@api_view(['PUT', 'PATCH'])
def project_edit(request, project_id):
    api_key = request.headers.get('x-api-key')
    user = User.objects.filter(api_key=api_key).first()

    if not user:
        return HttpResponse("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return HttpResponse("Project not found", status=404)

    project.name = request.PUT.get('name', project.name)
    project.description = request.PUT.get('description', project.description)
    project.save()

    return HttpResponse("Project Edit")

@api_view(['DELETE'])
def project_delete(request, project_id):
    api_key = request.headers.get('x-api-key')
    user = User.objects.filter(api_key=api_key).first()

    if not user:
        return HttpResponse("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return HttpResponse("Project not found", status=404)

    project.delete()
    return HttpResponse("Project Delete")

@api_view(['POST'])
def hypothesis_create(request, project_id):
    api_key = request.headers.get('x-api-key')
    user = User.objects.filter(api_key=api_key).first()

    if not user:
        return HttpResponse("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return HttpResponse("Project not found", status=404)

    # Create the hypothesis
    hypothesis = Hypothesis.objects.create(
        title=request.POST.get('title'),
        commit=request.POST.get('commit'),
        description=request.POST.get('description'),
        project=project
    )
    hypothesis.save()
    return HttpResponse("Hypothesis Create")

@api_view(['GET'])
def hypothesis_detail(request, hypothesis_id):
    return HttpResponse(f"Hypothesis Detail: {hypothesis_id}")


@api_view(['PUT', 'PATCH'])
def hypothesis_edit(request, hypothesis_id):
    return HttpResponse(f"Hypothesis Edit: {hypothesis_id}")


@api_view(['DELETE'])
def hypothesis_delete(request, hypothesis_id):
    return HttpResponse(f"Hypothesis Delete: {hypothesis_id}")

@api_view(['POST'])
def experiment_create(request, hypothesis_id):
    return HttpResponse(f"Experiment Create for Hypothesis: {hypothesis_id}")

@api_view(['GET'])
def experiment_detail(request, experiment_id):
    return HttpResponse(f"Experiment Detail: {experiment_id}")

@api_view(['PUT', 'PATCH'])
def experiment_edit(request, experiment_id):
    return HttpResponse(f"Experiment Edit: {experiment_id}")

@api_view(['DELETE'])
def experiment_delete(request, experiment_id):
    return HttpResponse(f"Experiment Delete: {experiment_id}")

@api_view(['POST'])
def result_create(request, experiment_id):
    return HttpResponse(f"Result Create for Experiment: {experiment_id}")

@api_view(['GET'])
def result_detail(request, result_id):
    return HttpResponse(f"Result Detail: {result_id}")

@api_view(['PUT', 'PATCH'])
def result_edit(request, result_id):
    return HttpResponse(f"Result Edit: {result_id}")

@api_view(['DELETE'])
def result_delete(request, result_id):
    return HttpResponse(f"Result Delete: {result_id}")

@api_view(['POST'])
def create_account(request):
    api_key = request.headers.get('x-api-key')
    print("Received API Key:", api_key)
    print("Expected ADMIN_API_KEY:", settings.ADMIN_API_KEY)
    if api_key != settings.ADMIN_API_KEY:
        return HttpResponse("Unauthorized", status=401)

    new_key = random.randint(100000, 999999)
    print(request.POST.get('username'))
    user = User.objects.create(username=request.POST.get('username'), api_key=new_key)
    user.save()
    return HttpResponse("Account Created api_key=" + str(new_key))

@api_view(['DELETE'])
def delete_account(request):
    return HttpResponse("Delete Account")



@require_GET
def project_results_by_accuracy(request, project_id, threshold):
    return HttpResponse(f"Project {project_id} Results with Accuracy >= {threshold}")

@require_GET
def experiments_no_results(request):
    return HttpResponse("Experiments with No Results")

@require_GET
def hypothesis_best_result(request, project_id, hypothesis_id):
    return HttpResponse(f"Best Result for Hypothesis {hypothesis_id} in Project {project_id}")

@require_GET
def results_training_time_under(request, time_seconds):
    return HttpResponse(f"Results with Training Time Under {time_seconds} seconds")
