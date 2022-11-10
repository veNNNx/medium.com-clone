from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length = 100)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    text = models.TextField()
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add = True)

    img = models.ImageField(upload_to='images/', blank=True, null=True)
    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return self.title 

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def __str__(self):
        return str(self.article.title)