

from rest_framework import viewsets,permissions


from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project, Hypotheses, Experiment, Result, User
import json
import random

'''

'''
#checks the api key from the request headers and returns the associated user or None if invalid
def check_api_key(request):
    api_key = request.headers.get('x-api-key')
    user = User.objects.filter(api_key=api_key).first()
    return user
#checks if the api key from the request headers matches the admin api key in settings
def check_admin_api_key(request):
    api_key = request.headers.get('x-api-key')
    return api_key == settings.ADMIN_API_KEY



@api_view(['GET'])
def index(request):
    return Response("Research Card Project Management System API")

## Account Management

@api_view(['POST'])
def create_account(request):
    print(request.POST)
    if check_admin_api_key(request) is False:
        return Response("Unauthorized", status=401)

    #if the requesting user is admin, create a new user with a random api key 

    new_key = random.randint(100000, 999999)
    print(request.POST.get('username'))
    user = User.objects.create(username=request.POST.get('username'), api_key=new_key)
    user.save()

    # return the new user's details including the api key

    return Response({'username': user.username, 'api_key': user.api_key})
    

@api_view(['DELETE'])
def delete_account(request, username):
    if check_admin_api_key(request) is False:
        return Response("Unauthorized", status=401)

    #if the requesting user is admin, delete the specified user by the username in the DELETE data

    username
    user = User.objects.filter(username=username).first()
    if not user:
        return Response("User not found", status=404)
    user.delete()
    return Response({'message': f'User {username} deleted'}) 


#For our convenience, an endpoint to list all accounts (admin only)
@api_view(['GET'])
def get_accounts(request):
    if check_admin_api_key(request) is False:
        return Response("Unauthorized", status=401)
    users = User.objects.all()
    return Response([user.to_json() for user in users])

#list the projects owned by or associated with the user identified by the api key in the request headers
@api_view(['GET'])
def project_list(request):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    projects = Project.objects.filter(owner=user)
    projects_associated = Project.objects.filter(associated_users=user)

    #seperate the owned and associated projects in the response

    json_data = {
        "total_projects": projects.count(),
        "projects_owned": [{"id": p.id, "name": p.name, "description": p.description} for p in projects],
        "projects_associated": [{"id": p.id, "name": p.name, "description": p.description} for p in projects_associated]
    }

    return Response(json_data)

## Project CRUD operations

#As opposed to the list above this shows all details of a specific project rather than just a summary 
@api_view(['GET'])
def project_detail(request, project_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.get(id=project_id)

    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    return Response(project.to_json())

@api_view(['POST'])
def project_create(request):
    user = check_api_key(request)

    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.create(
        name=request.POST.get('name'),
        description=request.POST.get('description'),
        owner=user
    )
    project.save()
    return Response({"message": "Project Created", "project_id": project.id})


#Projects can have multiple associated users who can view and add to the project but not delete it or manage users
@api_view(['PUT'])
def project_add_user(request, project_id):
    user = check_api_key(request)

    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return Response("Project not found", status=404)

    associate = request.POST.get('username')
    new_user = User.objects.filter(username=associate).first()
    if not new_user:
        return Response("User not found", status=404)

    project.associated_users.add(new_user)
    project.save()

    return Response({'message': f"User {associate} added to project {project.name}"})


#likewise the owner of the project can remove associated users
@api_view(['PUT'])
def project_remove_user(request, project_id):
    user = check_api_key(request)

    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return Response("Project not found", status=404)

    associate = request.POST.get('username')
    user = User.objects.filter(username=associate).first()
    if user not in project.associated_users.all():
        return Response("User not found", status=404)

    project.associated_users.remove(user)
    project.save()

    return Response({"message": f"User {associate} removed from project {project.name}"})

#edit the name and description of a project (only by the owner)
@api_view(['PUT'])
def project_edit(request, project_id):
    user = check_api_key(request)
    
    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return Response("Project not found", status=404)

    project.name = request.POST.get('name', project.name)
    project.description = request.POST.get('description', project.description)
    project.save()

    return Response({"message": "Project Edited", "project_id": project.id})

#delete a project (only by the owner)
@api_view(['DELETE'])
def project_delete(request, project_id):
    user = check_api_key(request)

    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id, owner=user).first()
    if not project:
        return Response("Project not found", status=404)

    project.delete()
    return Response({"message": "Project Deleted"})

## In-depth Project Views

@api_view(['GET'])
def hypothesis_list(request, project_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)
    hypotheses = Hypotheses.objects.filter(project=project)
    return Response([h.to_json() for h in hypotheses])

@api_view(['GET'])
def hypothesis_search(request, project_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    query = request.GET.get('q', '')
    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)
    hypotheses = Hypotheses.objects.filter(project=project, title__icontains=query)
    return Response([h.to_json() for h in hypotheses])

@api_view(['GET'])
def hypothesis_filter_by_keyword(request, project_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    keyword = request.GET.get('keyword', '')
    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)
    hypotheses = Hypotheses.objects.filter(project=project, description__icontains=keyword)
    return Response([h.to_json() for h in hypotheses])

@api_view(['GET'])
def experiment_list(request, project_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)
    experiments = Experiment.objects.filter(hypothesis__project=project)
    return Response([e.to_json() for e in experiments])

@api_view(['GET'])
def result_list(request, project_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)
    results = Result.objects.filter(experiment__hypothesis__project=project)
    return Response([r.to_json() for r in results])


## Hypothesis CRUD operations

#create a new hypothesis within a project (only by owner or associated users)
#A hypothesis consists of a title, commit hash i.e. to a code repo, description, and is linked to a specific project
@api_view(['POST'])
def hypothesis_create(request, project_id):
    user = check_api_key(request)

    if not user:
        return Response("Unauthorized", status=401)

    project = Project.objects.filter(id=project_id).first()

    if not project:
        return Response("Project not found", status=404)
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)
    # Create the hypothesis
    hypothesis = Hypotheses.objects.create(
        title=request.POST.get('title'),
        commit=request.POST.get('commit'),
        description=request.POST.get('description'),
        project=project
    )
    hypothesis.save()
    return Response({"message": "Hypothesis Created", "hypothesis_id": hypothesis.id})

#list the details of a specific hypothesis
@api_view(['GET'])
def hypothesis_detail(request, hypothesis_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    

    hypothesis = Hypotheses.objects.get(id=hypothesis_id)

    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    return Response(hypothesis.to_json())

#edit the details of a hypothesis (only by owner or associated users of the linked project)
@api_view(['PUT'])
def hypothesis_edit(request, hypothesis_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    hypothesis = Hypotheses.objects.get(id=hypothesis_id)

    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    hypothesis.title = request.POST.get('title', hypothesis.title)
    hypothesis.commit = request.POST.get('commit', hypothesis.commit)
    hypothesis.description = request.POST.get('description', hypothesis.description)
    hypothesis.save()

    return Response({"message": f"Hypothesis Edited", "hypothesis_id": hypothesis.id})

#delete a hypothesis (only by owner or associated users of the linked project)
@api_view(['DELETE'])
def hypothesis_delete(request, hypothesis_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    hypothesis = Hypotheses.objects.get(id=hypothesis_id)

    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)
    hypothesis.delete()
    return Response({"message": f"Hypothesis Deleted"})


## Experiment CRUD operations

#create a new experiment
#each experiement is linked to one of the hypotheses within a project
#an experiment consists of a description, type which can be SVM , Random Forest or Neural Network, Learning Rate, Batch Size, and Epochs
@api_view(['POST'])
def experiment_create(request, hypothesis_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    hypothesis = Hypotheses.objects.get(id=hypothesis_id)
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    # Create the experiment
    experiment = Experiment.objects.create(
        description=request.POST.get('description'),
        experiment_type=request.POST.get('experiment_type'),
        learning_rate=request.POST.get('learning_rate'),
        batch_size=request.POST.get('batch_size'),
        epochs=request.POST.get('epochs'),
        hypothesis=hypothesis
    )
    experiment.save()
    return Response({"message": "Experiment Created", "experiment_id": experiment.id})

#view the details of a specific experiment
@api_view(['GET'])
def experiment_detail(request, experiment_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    experiment = Experiment.objects.get(id=experiment_id)
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    return Response(experiment.to_json())

#edit any or all of the details of an experiment 
@api_view(['PUT'])
def experiment_edit(request, experiment_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    experiment = Experiment.objects.get(id=experiment_id)
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    experiment.description = request.POST.get('description', experiment.description)
    experiment.experiment_type = request.POST.get('experiment_type', experiment.experiment_type)
    experiment.learning_rate = request.POST.get('learning_rate', experiment.learning_rate)
    experiment.batch_size = request.POST.get('batch_size', experiment.batch_size)
    experiment.epochs = request.POST.get('epochs', experiment.epochs)
    experiment.save()

    return Response({"message": f"Experiment Edited", "experiment_id": experiment.id})

#delete the experiment given by its id
@api_view(['DELETE'])
def experiment_delete(request, experiment_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    experiment = Experiment.objects.get(id=experiment_id)
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    experiment.delete()
    return Response({"message": f"Experiment Deleted"})


## Result CRUD operations

#create a new result linked to an experiment
#each result consists of accuracy, loss, ROC, PR_AUC, weights_path, training_time, and a comment
#the weights path is a string so that it can be a path to a file or a URL to a cloud storage location where the training model weights are stored
@api_view(['POST'])
def result_create(request, experiment_id):
    print(request.POST)
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    experiment = Experiment.objects.get(id=experiment_id)
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    # Create the result
    result = Result.objects.create(
        accuracy=request.POST.get('accuracy'),
        loss=request.POST.get('loss'),
        ROC=request.POST.get('ROC'),
        PR_AUC=request.POST.get('PR_AUC'),
        weights_path=request.POST.get('weights_path'),
        training_time=request.POST.get('training_time'),
        experiment=experiment,
        comment=request.POST.get('comment', '')
    )
    result.save()


    return Response({"message": "Result Created", "result_id": result.id})

#view the details of a specific result
@api_view(['GET'])
def result_detail(request, result_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    result = Result.objects.get(id=result_id)
    experiment = result.experiment
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    return Response(result.to_json())


#edit any or all of the details of a result
@api_view(['PUT'])
def result_edit(request, result_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    result = Result.objects.get(id=result_id)
    experiment = result.experiment
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    result.accuracy = request.POST.get('accuracy', result.accuracy)
    result.loss = request.POST.get('loss', result.loss)
    result.ROC = request.POST.get('ROC', result.ROC)
    result.PR_AUC = request.POST.get('PR_AUC', result.PR_AUC)
    result.weights_path = request.POST.get('weights_path', result.weights_path)
    result.training_time = request.POST.get('training_time', result.training_time)
    result.comment = request.POST.get('comment', result.comment)
    result.save()
    

    return Response({"message": f"Result Edited", "result_id": result.id})


#delete the result given by its id
@api_view(['DELETE'])
def result_delete(request, result_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    result = Result.objects.get(id=result_id)
    experiment = result.experiment
    hypothesis = experiment.hypothesis
    project = hypothesis.project
    if project.owner != user and user not in project.associated_users.all():
        return Response("Forbidden", status=403)

    result.delete()
    return Response({"message": f"Result Deleted"})


## Specialized Queries


#For the given project return all results with accuracy above the given threshold, iff the user is owner or associated user of the project
@api_view(['GET'])
def project_results_by_accuracy(request, project_id, threshold):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)
    
    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)
    
    results = Result.objects.filter(experiment__hypothesis__project=project, accuracy__gt=threshold)
    return Response([r.to_json() for r in results])

#finds experiments that have no results associated with them and are owned by or associated with the user
#for finding experiments that were planned but never run or where results were not recorded
@api_view(['GET'])
def experiments_no_results(request):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    experiments = Experiment.objects.filter(results__isnull=True, hypothesis__project__owner=user) | Experiment.objects.filter(results__isnull=True, hypothesis__project__associated_users=user)
    experiments = experiments.distinct()
    return Response([e.to_json() for e in experiments])


#For a given hypothesis within a project return the best N results sorted by accuracy where the default value of N is 5, iff the user is owner or associated user of the project
@api_view(['GET'])
def hypothesis_best_result(request, project_id, hypothesis_id):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    N = int(request.GET.get('top_n', 5))

    project = Project.objects.filter(id=project_id).first()
    if not project or (project.owner != user and user not in project.associated_users.all()):
        return Response("Forbidden", status=403)

    hypothesis = Hypotheses.objects.filter(id=hypothesis_id, project=project).first()
    if not hypothesis:
        return Response("Hypothesis Not Found", status=404)

    best_results = Result.objects.filter(experiment__hypothesis=hypothesis).order_by('-accuracy')[:N]

    return Response([b.to_json() for b in best_results])


#Return all results across all projects owned by or associated with the user where the training time was under the specified number of seconds
#For finding experiments that ran quickly/efficiently
@api_view(['GET'])
def results_training_time_under(request, time_seconds):
    user = check_api_key(request)
    if not user:
        return Response("Unauthorized", status=401)

    results = Result.objects.filter(training_time__lt=time_seconds, experiment__hypothesis__project__owner=user) | Result.objects.filter(training_time__lt=time_seconds, experiment__hypothesis__project__associated_users=user)
    results = results.distinct()
    return Response([r.to_json() for r in results])
