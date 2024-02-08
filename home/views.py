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