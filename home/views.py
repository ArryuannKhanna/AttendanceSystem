from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

import cv2
import base64
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return render(request, 'index.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Username or email already exists'})
        user = User.objects.create(username=username,email=email,password=make_password(password))
        user.save()
        return redirect('home')
    return render(request, 'signup.html')

from django.shortcuts import render
from .models import User  # Assuming your user model is named 'User'

def dashboard(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        user = User.objects.get(email=email)
        classjoined = user.classjoined  # Remove () after classjoined and classcreated
        classcreated = user.classcreated
        return render(request, 'dashboard.html', {'classjoined': classjoined, 'classcreated': classcreated})  # Correct the syntax of render method

    elif request.method == 'POST':  # Change IF to elif and correct the syntax
        email = request.POST.get('email')
        classjoined = request.POST.get('classjoined')  # Correct the variable names
        classcreated = request.POST.get('classcreated')  # Correct the variable names
        user = User.objects.get(email=email)
        user.classjoined = classjoined  # Assign the new values to the user object
        user.classcreated = classcreated  # Assign the new values to the user object
        user.save()  # Save the changes to the user object
        return render(request, 'dashboard.html')  # Render the dashboard template

    else:
        # Handle other HTTP methods if necessary
        return render(request, 'dashboard.html')

def classroom(request):
    #Get attendace from the database
    if request.method == 'GET':
        email = request.GET.get('email')
        user = User.objects.get(email=email)
        attendace = user.attendace
        return render(request, 'dashboard.html', {'user': user, 'attendace': attendace})
    #Changes made by the admin
    elif request.method == 'POST':
        email = request.POST.get('email')

# @csrf_exempt
# def process_webcam(request):
#     if request.method == 'POST':
#         try:
#             # Extract base64 image data from POST request
#             data = request.POST.get('image')
#             encoded_data = data.split(',')[1]
#             nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
#             image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#
#             # Perform image processing using OpenCV (dummy example)
#             # For demonstration purposes, just flip the image horizontally
#             annotated_image = cv2.flip(image, 1)
#
#             # Convert annotated image to base64 string
#             _, encoded_annotated_image = cv2.imencode('.jpg', annotated_image)
#             annotated_image_base64 = base64.b64encode(encoded_annotated_image).decode()
#
#             return JsonResponse({'annotated_image': f'data:image/jpeg;base64,{annotated_image_base64}'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed for this endpoint.'})