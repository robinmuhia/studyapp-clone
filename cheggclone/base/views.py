from django.shortcuts import render

rooms = [
    {'id': 1,
    'name':"Let's learn python"},
    {'id': 2,
    'name':"Design with me #React,Mui,Next"},
    {'id': 3,
    'name':"Looking for frontend devs"}

]

def home(request:str):
    context = {'rooms':rooms}
    return render(request,'base/home.html',context)


def room(request:str,pk:str):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    
    context = {'room':room}
            
    return render(request,'base/room.html',context)