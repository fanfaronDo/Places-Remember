from django.contrib.auth.models import User
from django.db import models


class Remember(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(max_length=300, blank=True)
    img = models.ImageField(upload_to='places_remember/images', blank=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    #position =

    def __repr__(self):
        return self.title