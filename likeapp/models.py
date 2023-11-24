from django.db import models

from django.contrib.auth.models import User
# Create your models here.

from articleapp.models import Article


class LikeRecord(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='like_recode')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_recode')
    
    class Meta:
        unique_together = ('user','article')
    