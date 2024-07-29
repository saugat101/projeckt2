from django.db import models
from django.conf import settings
from core.models import Movie,User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user} rated {self.movie}: {self.rating}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review = models.TextField()

    class Meta:
        unique_together = ('user', 'movie')


    def __str__(self):
        return f"{self.user} reviewed {self.movie}"