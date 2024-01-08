from django.contrib.auth.models import User
from django.db import models

import uuid

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)   
    image = models.URLField(max_length=500) 
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    body = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=100)
   
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']

    
class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True) # filefield instead of imagefield since we have to deal with svg files
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['order']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return f'{self.author.username} : {self.body[:30]}'
