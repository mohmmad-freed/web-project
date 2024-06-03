from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD
=======
# Defining the choices for the days
>>>>>>> 71bb4904e745b8802ddf0793b6481aa13ea2d3bc
DAY_CHOICES = (
    ('S,T,T', 'Sunday, Tuesday, Thursday'),
    ('M,W', 'Monday, Wednesday')
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
<<<<<<< HEAD
=======
    completed_courses = models.ManyToManyField('Course', related_name='completed_students', blank=True)
>>>>>>> 71bb4904e745b8802ddf0793b6481aa13ea2d3bc
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
<<<<<<< HEAD
    room_no = models.CharField(max_length=10)
    is_completed = models.BooleanField(default=False)
=======
    room_no = models.CharField(max_length=10, default='4')
>>>>>>> 71bb4904e745b8802ddf0793b6481aa13ea2d3bc

    def __str__(self):
        return f"{self.course.name} - {self.days}"

    class Meta:
        unique_together = ('course', 'days', 'start_time', 'end_time', 'room_no')
