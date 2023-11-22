from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=20, null=False)
    image = models.ImageField(upload_to='project/', null=False)
    description = models.CharField(max_length=200, null=True)
    
    created_at = models.DateField(auto_now_add=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='project', null=True)
        
    def __str__(self):
        return f'{self.title}'