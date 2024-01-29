from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from projectapp.models import Project
from artistapp.models import Artist
from personapp.models import Person



class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='article', null=True)
    project = models.ManyToManyField(Project, related_name='article', blank=True)
    artist = models.ManyToManyField(Artist, related_name='article', blank=True)
    person = models.ManyToManyField(Person, related_name='article', blank=True)
    
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='article/', null=False)
    content = models.TextField(null=True)
    
    created_at = models.DateField(auto_now_add=True, null=True)
    date = models.DateField(blank=True, null=True)  # 필수 입력 필드
    datetime = models.DateTimeField(blank=True, null=True)  # DateField에서 DateTimeField로 변경
    
    like = models.IntegerField(default=0)
    hide = models.BooleanField(default=True)  # 임시저장 여부를 나타내는 필드
