from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import Movie

admin.site.register(User, UserAdmin)
admin.site.register(Movie)