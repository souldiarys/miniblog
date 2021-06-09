from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from .forms import LoginForm, SignUpForm, PostForm
from .models import Post

# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

# About
def about(request):
    return render(request, 'blog/about.html')

# Contact
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':groups})
    else:
        return redirect('login')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author.')
            user = form.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login in Successfully!!')
                    return redirect('dashboard')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return redirect('dashboard')

# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post = Post(title=title, desc=desc)
                post.save()
                return redirect('dashboard')
        else:
            form = PostForm()
        return render(request, 'core/addpost.html', {'form':form})
    else:
        return redirect('login')

# Update Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'core/updatepost.html', {'form':form})
    else:
        return redirect('login')

# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return redirect('dashboard')
    else:
        return redirect('login')