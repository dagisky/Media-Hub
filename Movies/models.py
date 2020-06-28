from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import shelve

class Movie(models.Model):
    Name=models.CharField(max_length=300)
    Year=models.CharField(max_length=5)
    Plot=models.CharField(max_length=1500)
    Genre=models.CharField(max_length=250)
    Imdb_rating=models.FloatField(default=0.0)
    Plot_outline=models.CharField(max_length=1000,default=None)
    Director=models.CharField(max_length=50,default=None)
    Poster=models.FileField()
    Path=models.CharField(max_length=100)
    trailer=models.CharField(max_length=150,default=None,null=True,blank=True)

    def __str__(self):
        return self.Name


class Ratings(models.Model):
    Rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5),MinValueValidator(0)])
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.Rating
        