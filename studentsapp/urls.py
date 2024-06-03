from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('account/', views.account, name='account'),
    path('accountAdmin/', views.accountAdmin, name='accountAdmin'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('addShedular/', views.addShedular, name='addShedular'),
    path('courseAdmin/', views.courseAdmin, name='courseAdmin'),
    path('courses/', views.courses, name='courses'),
    path('courseSchedular/', views.courseSchedular, name='courseSchedular'),
    path('coursesstudents/', views.coursesstudents, name='coursesstudents'),
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),
    path('register/', views.register, name='register'),
    path('schedular/', views.schedular, name='schedular'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),

]
