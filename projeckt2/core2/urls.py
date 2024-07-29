from django.urls import path
from .views import movies_by_genre

urlpatterns = [
    path('movies/genre/<str:genre>/', movies_by_genre, name='movies_by_genre'),
]
