from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from projectapp.models import Project
from artistapp.models import Artist

class P_Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='P_subscripton')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='P_subscripton')
    
    class Meta:
        unique_together = ('user', 'project')

class A_Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='A_subscripton')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='A_subscripton')
    
    class Meta:
        unique_together = ('user', 'artist')
        
        
        