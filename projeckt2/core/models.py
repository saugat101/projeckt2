from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUserManager(BaseUserManager):

    # profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)
    
    def delete_profile_picture(self):
        if self.profile_picture and self.profile_picture.name != 'profile_pictures/default.jpg':
            self.profile_picture.delete()

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

class Movie(models.Model):
    movie_id=models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    credits = models.TextField(null=True, blank=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    budget = models.BigIntegerField(blank=True, null=True)
    poster_url = models.URLField(max_length=200, blank=True, null=True)
    backdrop_url = models.URLField(max_length=200, blank=True, null=True)
    poster = models.ImageField(upload_to='posters/', default='posters/default_poster.jpg', null=True)
    trailer = models.URLField(max_length=200, blank=True, null=True)
    homepage = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

# class Rating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     rating = models.IntegerField()

    # class Meta:
    #         constraints = [
    #         models.UniqueConstraint(fields=['user', 'movie'], name='unique_user_rating')
    #     ]

    # def __str__(self):
    #     return f"{self.user} rated {self.movie}: {self.rating}"


# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     review = models.TextField()

#     class Meta:
#             constraints = [
#             models.UniqueConstraint(fields=['user', 'movie'], name='unique_user_review')
        # ]

    # def __str__(self):
    #     return f"Review by {self.user} on {self.movie}"