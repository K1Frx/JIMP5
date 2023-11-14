from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    director = models.CharField(max_length=64)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(unique=True, max_length=64)
    
    def __str__(self):
        return self.name