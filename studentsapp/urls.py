from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('register_course/', views.register_course, name='register_course'),
    path('courses/', views.courses, name='courses'),
    path('account/', views.account, name='account'),
    path('accountAdmin/', views.accountAdmin, name='accountAdmin'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('addShedular/', views.addShedular, name='addShedular'),
    path('courseAdmin/', views.courseAdmin, name='courseAdmin'),
    path('coursesstudents/', views.coursesstudents, name='coursesstudents'),
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),
    path('schedular/', views.schedular, name='schedular'),
]
