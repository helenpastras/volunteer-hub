from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User



class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Opportunity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    location = models.CharField(max_length=100)
    date = models.DateField()
    tags = models.ManyToManyField(Tag)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    created_at = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('opportunity-detail', kwargs={'pk': self.pk})


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'opportunity') 

    def __str__(self):
        return f"{self.user.username} liked {self.opportunity.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'opportunity')  # Prevent duplicate bookmarks

    def __str__(self):
        return f"{self.user.username} bookmarked {self.opportunity.title}"