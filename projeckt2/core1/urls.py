from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('ratings/create/', RatingCreateView.as_view(), name='rating-create'),
    path('ratings/update/<int:pk>/', RatingUpdateView.as_view(), name='rating-update'),
    path('ratings/delete/<int:pk>/', RatingDeleteView.as_view(), name='rating-delete'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/update/<int:pk>/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review-delete'),
]