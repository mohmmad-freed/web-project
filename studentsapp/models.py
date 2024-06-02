from django.db import models

# Create your models here.



class CourseSchedule(models.Model):
    days = models.CharField(max_length=50)
    startTime = models.TimeField()
    endTime = models.TimeField()
    roomNo = models.CharField(max_length=50)

class Course(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    prerequisites = models.TextField()
    instructor = models.CharField(max_length=100)
    capacity = models.IntegerField()
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE)

class Student(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()

class StudentReg(models.Model):
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
