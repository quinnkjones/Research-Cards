from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    api_key = models.CharField(max_length=255, unique=True)
   
    
    def __str__(self):
        return self.username
    

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    def __str__(self):
        return self.name
    
class Hypothesis(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    commit = models.TextField(blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='hypotheses')
    
    def __str__(self):
        return self.title
    
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

class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    learning_rate = models.FloatField(null=True, blank=True)
    batch_size = models.IntegerField(null=True, blank=True)
    epochs = models.IntegerField(null=True, blank=True)

    hypothesis = models.ForeignKey(Hypothesis, on_delete=models.CASCADE, related_name='experiments')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='experiments', null=True, blank=True)

    def __str__(self):
        return self.title