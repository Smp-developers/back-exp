from django.contrib import admin

from project_api.models import  Courses, User

# Register your models here.

admin.site.register(User)
admin.site.register(Courses)