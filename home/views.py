from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

# Create your views here.

def home(request):
    return render(request, 'index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        print(firstname)
        lastname  = request.POST.get('last_name')
        print(lastname)
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username or email already exists'})
        user = User.objects.create(username=username,password=make_password(password))
        user.save()
        return redirect('home')
    return render(request, 'signup.html')
