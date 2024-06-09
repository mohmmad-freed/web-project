from django.contrib import admin
from .models import *



class CourseAdmin(admin.ModelAdmin):
    list_display=["code",'name','get_pre','scheduled','get_students_count']
    search_fields = ['code__istartswith','name__istartswith']
    def get_pre(self,obj):
        if obj.prerequisites.count() ==0:
            return "null"
        else:
            return ", ".join([prerequisite.name for prerequisite in obj.prerequisites.all()])
    get_pre.short_description = 'Prerequisites'
    def get_students_count(self,obj):
      return obj.students.count()
    get_students_count.short_description = 'Students count'

class StudentAdmin(admin.ModelAdmin):
    search_fields = ["id__istartswith", "user__username__startswith"]
    list_display = ["id", "get_username", "get_email"]
    ordering=["id"]
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'date_created', 'active', 'deadline_date']
    list_filter = ['active', 'date_created']
    search_fields = ['message']
class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ['days', 'start_time', 'end_time', 'room_no']
    list_filter = ['days']
    search_fields = ['room_no','days']
# Register your models here.
admin.site.register(Student,StudentAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseSchedule,CourseScheduleAdmin)
admin.site.register(StudentRegistration)
admin.site.register(Notification,NotificationAdmin)
