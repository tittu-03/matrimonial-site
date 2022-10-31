import os

from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse
from . import models
# from .forms import *
from .models import *
from django.core.mail import send_mail
from matrimonial.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from django.contrib.auth import authenticate

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        image=request.FILES['image']
        password1=request.POST.get('password1')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        occupation=request.POST.get('occupation')
        looking_for=request.POST.get('looking_for')
        bio=request.POST.get('bio')
        if password == password1:
            if User.objects.filter(email=email).first():
                messages.success(request,'email already exist')
                return redirect('registration.html')
            user_obj=User(username=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            a=regmodel.objects.create(user=user_obj,auth_token=auth_token,name=name,phone=phone,gender=gender,
                                     image=image,dob=dob,occupation=occupation,looking_for=looking_for,bio=bio)
            a.save()
            send_mail_regis(email,auth_token)
            return redirect (tokensend)
        else :
            messages.success(request, 'Password Mismatch')
    return render(request,'registration.html')

def send_mail_regis(email,auth_token):
    subject='your account has been verified'
    message=f'past the link to verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from=settings.EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=regmodel.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'Your account has been verified')
        return redirect(success)
    else:
        return redirect('/error')

def success(request):
    return render(request,'success.html')

def tokensend(request):
    return render(request,'tockensend.html')

def error(request):
    return render(request,'errorpage.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email).first()
        if user_obj is None:
            messages.success(request, 'user not found')
            return redirect(login)
        profile_obj = regmodel.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'profile not verified plz check your email')
            return redirect(login)
        user = authenticate(username=email, password=password)
        if user is None:
            messages.success(request, 'wrong password or username')
            return redirect(login)
        b=regmodel.objects.filter(user=user)
        li = []
        for i in b:
            path = i.image
            li.append(str(path).split('/')[-1])
        return render(request,'user_profile.html',{'profile':b,'z':li})
        # return HttpResponse('success')
    return render(request, 'login.html')

def user_profile(request):
    return render(request,'user_profile.html')

def profile_edit(request,auth_token,username):
    if request.method=='POST':
        a=regmodel.objects.filter(auth_token=auth_token).first()
        a.user.username=request.POST.get('email')
        a.name=request.POST.get('name')
        a.phone = request.POST.get('phone')
        a.dob = request.POST.get('dob')
        a.gender = request.POST.get('gender')
        a.occupation = request.POST.get('occupation')
        a.looking_for = request.POST.get('looking_for')
        a.bio = request.POST.get('bio')
        if len(request.FILES)==0:
            a.image=a.image
        else:
            os.remove(a.image.path)
            a.image=request.FILES['image']
        if a.user.username!=username:
            send_mail_regis(username,auth_token)
            a.is_verified=False
            a.user.save()
            a.save()
            return render(request,'tockensend.html')
        a.user.save()
        a.save()
        z = regmodel.objects.filter(auth_token=auth_token)
        li = []
        for i in z:
            path = i.image
            li.append(str(path).split('/')[-1])
        return render(request, 'user_profile.html', {'profile': z,'z': li})
    x = regmodel.objects.filter(auth_token=auth_token)
    li = []
    for i in x:
        path = i.image
        li.append(str(path).split('/')[-1])
    return render(request, 'profile_edit.html', {'profile': x,'x': li})