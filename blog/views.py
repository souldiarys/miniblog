from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from .forms import SignUpForm

# Home
def home(request):
    return render(request, 'blog/home.html')

# About
def about(request):
    return render(request, 'blog/about.html')

# Contact
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard
def dashboard(request):
    return render(request, 'blog/dashboard.html')

# Logout
def user_logout(request):
    return HttpResponseRedirect('/')

# Signup
def signup(request):
    form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

# Login
def user_login(request):
    return render(request, 'blog/login.html')
