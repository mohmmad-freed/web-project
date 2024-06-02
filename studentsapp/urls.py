from django.urls import path
from . import views


urlpatterns = [
    path('',views.login ),
    path('account/',views.account ),
    path('accountAdmin/',views.accountAdmin ),
    path('addCourse/',views.addCourse ),
    path('addShedular/',views.addShedular ),
    path('courseAdmin/',views.courseAdmin ),
    path('courses/',views.courses ),
    path('courseSchedular/',views.courseSchedular ),
    path('coursesstudents/',views.coursesstudents ),
    path('homeAdmin/',views.homeAdmin ),
    path('register/',views.register ),
    path('schedular/',views.schedular),
    path('home/',views.home ),
    
    
]
