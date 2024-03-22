from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Story(models.Model):
    #key = models.AutoField(primary_key=True, unique=True)
    headline = models.CharField(max_length=64)
    categories = [('pol', 'Politics'),('art','Art'),('tech','Technology'),('trivia','Trivial')]
    category = models.CharField(max_length=32, choices=categories, default='unknown')
    regions = [('uk', 'UK News'),('eu', 'European News'),('w', 'World News')]
    region = models.CharField(max_length=32, choices=regions, default='unknown')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=128)


