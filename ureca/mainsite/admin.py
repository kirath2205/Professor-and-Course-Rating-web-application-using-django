from django.contrib import admin

# Register your models here.
from .models import Corse,Contact,Modules,CourseComment,Rating3

admin.site.register(Contact)
admin.site.register((Modules,CourseComment,Rating3))

