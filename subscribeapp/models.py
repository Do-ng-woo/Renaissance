from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from projectapp.models import Project

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscripton')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='subscripton')
    
    class Meta:
        unique_together = ('user', 'project')