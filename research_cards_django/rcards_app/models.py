from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
   
    
    def __str__(self):
        return self.username
    
    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "api_key": self.api_key,
        }
    

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    associated_users = models.ManyToManyField(User, related_name='helpers', blank=True)

    def __str__(self):
        return self.name
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "owner": self.owner.username,
            "associated_users": [user.username for user in self.associated_users.all()],
        }
    
class Hypotheses(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    commit = models.TextField(blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='hypotheses')
    
    def __str__(self):
        return self.title
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "commit": self.commit,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "project_id": self.project.id,
        }
    
class Result(models.Model):
    id = models.AutoField(primary_key=True)
    accuracy = models.FloatField(null=True, blank=False)
    loss = models.FloatField(null=True, blank=False)
    ROC = models.FloatField(null=True, blank=True)
    PR_AUC = models.FloatField(null=True, blank=True)
    weights_path = models.TextField(blank=True)  # path to saved model weights
    training_time = models.FloatField(null=True, blank=True)  # in seconds      
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE, related_name='results')
    comment = models.TextField(blank=True)


    def __str__(self):
        return f"Result {self.id}"
    
    def to_json(self):
        return {
            "id": self.id,
            "accuracy": self.accuracy,
            "loss": self.loss,
            "ROC": self.ROC,
            "PR_AUC": self.PR_AUC,
            "weights_path": self.weights_path,
            "training_time": self.training_time,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "experiment_id": self.experiment.id,
            "comment": self.comment,
        }

class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    svm_type = 'svm'
    random_forest_type = 'rf'
    neural_network_type = 'nn'
    experiment_types = {
        (svm_type, 'Support Vector Machine'),
        (random_forest_type, 'Random Forest'),
        (neural_network_type, 'Neural Network'),
    }
    experiment_type = models.CharField(max_length=3, choices=experiment_types, default=svm_type)

    learning_rate = models.FloatField(null=True, blank=True)
    batch_size = models.IntegerField(null=True, blank=True)
    epochs = models.IntegerField(null=True, blank=True)

    hypothesis = models.ForeignKey(Hypotheses, on_delete=models.CASCADE, related_name='experiments')
    

    def __str__(self):
        return self.title
    
    def to_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "experiment_type": self.experiment_type,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "epochs": self.epochs,
            "hypothesis_id": self.hypothesis.id,
            
        }