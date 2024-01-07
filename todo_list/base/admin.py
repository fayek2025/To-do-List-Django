from django.contrib import admin
from .models import Task
# Register your models here.
#we need register our database with admin panel
admin.site.register(Task)