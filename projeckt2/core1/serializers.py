from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.urls import reverse
from django.contrib.auth import get_user_model

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'movie', 'rating']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
            user=validated_data['user'],
            movie=validated_data['movie'],
            defaults={'rating': validated_data['rating']}
        )
        return rating
    
    def update_movie_avg_rating(self, movie):
        rating = Rating.objects.filter(movie=movie)
        avg_rating = rating.aggregate(models.Avg('rating'))['rating__avg']
        vote_count = rating.count()
        movie.avg_rating = avg_rating
        movie.vote_count = vote_count
        movie.save()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'movie', 'review']

    def create(self, validated_data):
        review, created = Review.objects.update_or_create(
            user=validated_data['user'],
            movie=validated_data['movie'],
            defaults={'review': validated_data['review']}
        )
        return review