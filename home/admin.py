from django.contrib import admin
from .models import CustomUser, Classroom, Attendance

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Classroom)
admin.site.register(Attendance)