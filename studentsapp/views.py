from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.
def login(request):
    return render(request,"studentsapp/login.html")

def home(request):
    return render(request,"studentsapp/home.html")

def account(request):
    return render(request,"studentsapp/account.html")

def accountAdmin(request):
    return render(request,"studentsapp/accountAdmin.html")

def addCourse(request):
    return render(request,"studentsapp/addCourse.html")

def addShedular(request):
    return render(request,"studentsapp/addShedular.html")

def courseAdmin(request):
    return render(request,"studentsapp/courseAdmin.html")

def courses(request):
    return render(request,"studentsapp/courses.html")

def courseSchedular(request):
    return render(request,"studentsapp/courseSchedular.html")

def coursesstudents(request):
    return render(request,"studentsapp/coursesstudents.html")

def homeAdmin(request):
    return render(request,"studentsapp/homeAdmin.html")

def register(request):
    return render(request,"studentsapp/register.html")


def schedular(request):
    return render(request,"studentsapp/schedular.html")


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'studentsapp/login.html', {'form': form})