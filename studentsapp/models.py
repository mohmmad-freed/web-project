from django.db import models
from django.contrib.auth.models import User

# Defining the choices for the days
DAY_CHOICES = (
    ('S,T,T', 'Sunday, Tuesday, Thursday'),
    ('M,W', 'Monday, Wednesday')
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    completed_courses = models.ManyToManyField('Course', related_name='completed_students', blank=True)
    schedules = models.ManyToManyField('CourseSchedule', related_name='students')

    def __str__(self):
        return self.name

class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor_name = models.CharField(max_length=100)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.course_code} - {self.name}"

class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    days = models.CharField(max_length=7, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(max_length=10, default='4')

    def __str__(self):
        return f"{self.course.name} - {self.days}"

    class Meta:
        unique_together = ('course', 'days', 'start_time', 'end_time', 'room_no')
