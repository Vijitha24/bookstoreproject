from django.contrib.auth.models import User
from django.contrib import messages, auth

from django.shortcuts import render, redirect



# Create your views here.

def front_page(request):
    return render(request, 'login/home.html')
def Register_user(request):
    if request.method=='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email= request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password==c_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'user name already exist')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'mail id already exist')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save()
            return redirect('login')
        else:
            messages.info(request,'Password not match')
            return redirect('register')
    return render(request,'login/register.html')

def loginuser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('userbooklist')
        else:
            messages.info(request,'Please provide correct detais')
            return redirect('login')
    return render(request,'login/login.html')
def logout (request):
    auth.logout(request)
    return redirect('login')




