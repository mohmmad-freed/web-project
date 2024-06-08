from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)

admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(StudentRegistration)
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'date_created', 'active', 'deadline_date']
    list_filter = ['active', 'date_created']
    search_fields = ['message']
