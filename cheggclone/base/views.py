from django.shortcuts import render
from .models import Room


def home(request:str):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request,'base/home.html',context)


def room(request:str,pk:str):
    room = Room.objects.get(id = pk)
    
    context = {'room':room}
            
    return render(request,'base/room.html',context)