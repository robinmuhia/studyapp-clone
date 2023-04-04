from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Room,Topic
from django.contrib.auth.models import User
from .forms import RoomForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def login_page(request:object):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')  
    
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'User does not exist')
            
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not match with the records in our database')
            
    context ={'page':page }
    return render(request,'base/login_register.html',context)    
    

def logout_user(request:object):
    logout(request)
    return redirect('home')
    

def register_user(request:object):
    form = UserCreationForm()
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!!')
        
    context ={'form' : form}
    return render(request,'base/login_register.html',context)
    
    
def home(request:object):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q)|
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics,'room_count':room_count}    
    return render(request,'base/home.html',context)


def room(request:object,pk:str):
    room = Room.objects.get(id = pk)
    
    context = {'room':room}
            
    return render(request,'base/room.html',context)


@login_required(login_url='login')
def create_room(request:object):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def update_room(request:object, pk:str):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('Invalid credentials to execute requested action!!')
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def delete_room(request:object,pk:str):
    room = Room.objects.get(id=pk)
    if request.User != room.user:
        return HttpResponse('Invalid credentials to execute requested action!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})