from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from core.models import Movie

def movies_by_genre(request, genre):
    movies = Movie.objects.filter(genres__icontains=genre)
    movie_list = list(movies.values('id', 'title', 'genres'))
    return JsonResponse(movie_list, safe=False)
