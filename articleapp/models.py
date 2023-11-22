from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from projectapp.models import Project
from artistapp.models import Artist

class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='article', null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='article', null=True)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, related_name='article', null=True)
    
        
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='article/', null=False)
    content = models.TextField(null=True)
    
    created_at = models.DateField(auto_now_add=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.DateField(blank=True, null=True)
