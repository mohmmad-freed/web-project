from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)

admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(StudentRegistration)