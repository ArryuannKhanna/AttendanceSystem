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

# we dont have to render any page, we have to return the response

def loginUser(request):    
    if request.method == 'POST':    #login user
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'Logged In successfully'})

        return JsonResponse({'User not found'}, status=404)

def registerUser(request):     
    if request.method == 'POST':    #register user
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photos = request.POST.get('photo')
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Username or email already exists'})
        user = User.objects.create(username=username,email=email,password=make_password(password))
        user.save()
        return JsonResponse({'Registered successfully'})

from django.shortcuts import render
from .models import User 

def getDashboardDetails(request): 
    if request.method == 'GET': # get dashboard details of users
        email = request.GET.get('email')
        user = User.objects.get(email=email)
        username = user.username
        joinedClasses = user.joinedClasses
        createdClasses = user.createdClasses
        data = {
            'joinedClasses': joinedClasses,
            'createdClasses': createdClass
        }
        return JsonResponse(data)

def joinClassroom(request):
    if request.method == 'POST':  
        email = request.POST.get('email')   # we dont take input email from user
        joinedClasses = request.POST.get('classCode')
        user = User.objects.get(email=email)
        user.joinedClasses = joinedClasses  # add the joined class to list

        user.save()
        return JsonResponse({'Class Joined successfully'}, status=200)    # what to send??


def createClassroom(request):
    if request.method == 'POST': 
        email = request.POST.get('email')
        className = request.POST.get('className')
        #handle making a new classroom
        user = User.objects.get(email=email)
        user.createdClasses = createdClasses    # add the created class to list
        user.save()
        return JsonResponse({'Class Created successfully'}, status=200)    # what to send??

    else:
        return render(request, 'dashboard.html')

def handleClassroomRequests(request, classCode):
    if request.method == 'POST':    # update attendance
        email = request.GET.get('email')
        studentList = request.GET.get('studentList')
        classDetails = Class.objects.get(classCode=classCode)
        attendace = user.attendace

        return JsonResponse({'Attendance saved successfully'}, status=200)
    elif request.method == 'GET':   #get class Details
        classDetails = Class.objects.get(classCode=classCode)

        return JsonResponse(classDetails)






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