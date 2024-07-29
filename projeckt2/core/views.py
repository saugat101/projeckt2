from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Q
from rest_framework.decorators import api_view
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, Http404,FileResponse
from django.shortcuts import get_object_or_404
import os
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
import pickle


# with open('models/movies.pkl', 'rb') as f:
#      models= pickle.load(f)
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'id':user.id}, status=status.HTTP_200_OK)
    
@csrf_protect
@ensure_csrf_cookie
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return Response({'error': 'Only POST method is allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class MoviePagination(PageNumberPagination):
    page_size = 100
class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class TopMoviesList(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        
        return Movie.objects.all().order_by('-avg_rating')[:10]  # Adjust the limit as needed
    
@api_view(['GET'])
def search_movies(request):
    query = request.GET.get('query', '')
    if query:
        # model_output=models.recommend(query)
        movies = Movie.objects.filter(title=query)
    else:
        movies = Movie.objects.none()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer

class PopularNowMoviesList(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        recent_days = 10000  # Define the period for "recently released"
        recent_date = timezone.now().date() - timedelta(days=recent_days)
        return Movie.objects.filter(
            release_date__gte=recent_date,
            avg_rating__gte=3.5
        ).order_by('-release_date')
    
# class ProfilePictureView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, *args, **kwargs):
#         user = request.user
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         user = request.user
#         user.delete_profile_picture()
#         user.profile_picture = 'profile_pictures/default.jpg'
#         user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)