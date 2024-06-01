from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return render(request,"studentsapp/login.html")
def users(request):
    return HttpResponse("users page")
def about(request):
    return HttpResponse("about page")