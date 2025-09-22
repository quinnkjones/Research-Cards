from django.urls import include, path

from . import views







urlpatterns = [

    path('api-auth/', include('rest_framework.urls')),
    path("", views.index, name="index"),

    path("projects/", views.project_list, name="project_list"),


    #set of urls for managing a project CRUD and adding/removing users
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<int:project_id>/edit/", views.project_edit, name="project_edit"),
    path("projects/<int:project_id>/delete/", views.project_delete, name="project_delete"),
    path("projects/<int:project_id>/add_user/", views.project_add_user, name="project_add_user"),
    path("projects/<int:project_id>/remove_user/", views.project_remove_user, name="project_remove_user"),
    
    #urls for viewing and searching hypotheses, experiments, and results within a project
    path("projects/<int:project_id>/hypotheses/", views.hypothesis_list, name="hypothesis_list"),
    path("projects/<int:project_id>/hypotheses/search/", views.hypothesis_search, name="hypothesis_search"),
    path("projects/<int:project_id>/hypotheses/filter_by_keyword/", views.hypothesis_filter_by_keyword, name="hypothesis_filter_by_keyword"),
    path("projects/<int:project_id>/experiments/", views.experiment_list, name="experiment_list"),
    path("projects/<int:project_id>/results/", views.result_list, name="result_list"),

    #urls for creating, viewing, editing, and deleting hypotheses
    path("projects/<int:project_id>/hypotheses/create/", views.hypothesis_create, name="hypothesis_create"),
    path("hypotheses/<int:hypothesis_id>/", views.hypothesis_detail, name="hypothesis_detail"),
    path("hypotheses/<int:hypothesis_id>/edit/", views.hypothesis_edit, name="hypothesis_edit"),
    path("hypotheses/<int:hypothesis_id>/delete/", views.hypothesis_delete, name="hypothesis_delete"),

    #urls for creating, viewing, editing, and deleting experiments linked to a hypothesis
    path("hypotheses/<int:hypothesis_id>/experiments/create/", views.experiment_create, name="experiment_create"),
    path("experiments/<int:experiment_id>/", views.experiment_detail, name="experiment_detail"),
    path("experiments/<int:experiment_id>/edit/", views.experiment_edit, name="experiment_edit"),
    path("experiments/<int:experiment_id>/delete/", views.experiment_delete, name="experiment_delete"),
    
    #urls for creating, viewing, editing, and deleting results linked to an experiment
    path("experiments/<int:experiment_id>/results/create/", views.result_create, name="result_create"),
    path("results/<int:result_id>/", views.result_detail, name="result_detail"),
    path("results/<int:result_id>/edit/", views.result_edit, name="result_edit"),
    path("results/<int:result_id>/delete/", views.result_delete, name="result_delete"),

    #account management
    path("accounts/create/", views.create_account, name="create_account"),
    path("accounts/<str:username>/delete/", views.delete_account, name="delete_account"),
    path("accounts/", views.get_accounts, name="get_accounts"),

    # specialized queries that have more complicated logic or require joining data across multiple tables and return specific filtered data sets
    path("projects/<int:project_id>/results/accuracy_<str:threshold>/", views.project_results_by_accuracy, name="project_results_by_accuracy"),
    path("experiments/no_results/", views.experiments_no_results, name="experiments_no_results"),
    path("projects/<int:project_id>/hypotheses/<int:hypothesis_id>/best_result/", views.hypothesis_best_result, name="hypothesis_best_result"),
    path("results/training_time_under/<int:time_seconds>/", views.results_training_time_under, name="results_training_time_under"),


    #basics



]