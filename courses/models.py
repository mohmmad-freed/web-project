from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class Student(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.user.username

class CourseSchedule(models.Model):
    DAY_CHOICES = (
        ('S,T,T', 'Sunday, Tuesday, Thursday'),
        ('M,W', 'Monday, Wednesday')
    )
    
    days = models.CharField(max_length=50, null=True, choices=DAY_CHOICES)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    room_no = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.days} ({self.start_time} - {self.end_time})"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time')

class Course(models.Model):
    code = models.CharField(max_length=90, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    instructor = models.CharField(max_length=100, null=True)
    scheduled = models.ForeignKey(CourseSchedule, on_delete=models.PROTECT, related_name='courses')
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    capacity = models.IntegerField(null=True)
    students = models.ManyToManyField(Student, related_name='courses',blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.capacity < 0:
            raise ValidationError('Capacity must be a positive number')

class StudentRegistrationManager(models.Manager):
    def create_registration(self, student, course):
        if StudentRegistration.objects.filter(student=student, course=course).exists():
            raise ValidationError('Student is already registered in this course')
        if course.prerequisites.exists() and not all(prerequisite in student.courses.all() for prerequisite in course.prerequisites.all()):
            raise ValidationError('Student does not meet the prerequisites for this course')
        registration = self.create(student=student, course=course)
        return registration

class StudentRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='registrations')
    completed = models.BooleanField(default=False)

    objects = StudentRegistrationManager()

    def __str__(self):
        student_name = self.student.user.username if self.student and self.student.user else "Unknown student"
        course_code = self.course.code if self.course else "Unknown course"
        return f"{student_name} - {course_code}"

    class Meta:
        unique_together = ('student', 'course')

class Notification(models.Model):
    message = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    deadline_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification created on {self.date_created.strftime('%Y-%m-%d')} - Active: {self.active}"