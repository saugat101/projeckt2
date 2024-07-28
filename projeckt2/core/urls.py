from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('top-movies/', TopMoviesList.as_view(), name='top-movies'),
    path('search-movies/', search_movies, name='search-movies'),
    path('recent-movies/', MovieList.as_view(), name='movie-list'),
    path('popular-now/', PopularNowMoviesList.as_view(), name='popular-now'),
    # path('api/profile/picture/', ProfilePictureView.as_view(), name='profile-picture'),
]