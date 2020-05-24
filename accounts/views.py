from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.

def signup(req):
    if req.method == 'POST':
        if req.POST['password1'] == req.POST['password2']:
            try:
                user = User.objects.get(username=req.POST['username'])
                options = {
                    'error': 'Username already has been taken'
                }
                return render(req, 'accounts/signup.html', options)
            except User.DoesNotExist:
                user = User.objects.create_user(req.POST['username'],
                                                password=req.POST['password1'])
                auth.login(req, user)
                return redirect('home')
        else:
            options = {
                'error': 'Passwords must match'
            }
            return render(req, 'accounts/signup.html', options)
    else:
        return render(req, 'accounts/signup.html')


def login(req):
    if req.method == "POST":
        user = auth.authenticate(username=req.POST['username'],
                                 password=req.POST['password'])
        if user is not None:
            auth.login(req, user)
            return redirect('home')
        else:
            options = {
                'error': 'username or password is invalid'
            }
            return render(req, 'accounts/login.html', options)

    else:
        return render(req, 'accounts/login.html')


def logout(req):
    if req.method == "POST":
        auth.logout(req)
        return render(req, 'accounts/login.html')
