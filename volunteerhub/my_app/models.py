from django.db import models
from django.urls import reverse

# Create your models here.
class Opportunity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    location = models.CharField(max_length=100)
    date = models.DateField
    tags = models.CharField(max_length=100)
    # createdBy = models.ManyToManyField(User)
    createdAt = models.DateTimeField

    def __str__(self):
        return self.name
    
