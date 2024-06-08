# courses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('my_courses/', views.my_courses, name="my_courses"),
    path('homeAdmin/', views.homeAdmin, name="homeAdmin"),
    path('home/', views.home, name="home"),
    path('', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('register_course/<str:course_code>/', views.register_course, name="register_course"),
    path('profile/', views.profile, name="profile"),
    path('course_report/', views.course_report, name="course_report"),
    path('delete_course/<str:course_code>/', views.delete_course, name="delete_course"),
    path('addcourse/', views.add_course, name='add_course'),
    path('course_list/', views.course_lista, name='course_list'),
    path('addschedule/', views.add_schedule, name='add_schedule'),
    path('schedule_list/', views.schedule_list, name='schedule_list'),
    path('student_course_list/', views.student_course_list, name='student_course_list'),
    path('logout/', views.logout_view, name="logout"),
    path('courses/', views.courses, name="courses"),
    path('remove&editcourse/', views.removeeditcourse, name='removeeditcourse'),

]
