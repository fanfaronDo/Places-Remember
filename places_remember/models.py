from django.db import models


class Remember(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(max_length=300, blank=True)
    img = models.ImageField(upload_to="places_remember/images",
                            default='places_remember/static/places_remember/avatar_default.png')
    #position =

    def __repr__(self):
        return self.title