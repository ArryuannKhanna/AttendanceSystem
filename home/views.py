import random

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

import cv2
import base64
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import random
from .models import Classroom

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Retrieve user object from database
        user = CustomUser.objects.filter(email=email).first()

        # Check if user exists and password is correct
        if user is None or not check_password(password, user.password):
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        # Login user
        login(request, user)

        # Set cookie
        response = JsonResponse({'message': 'Login successful'})
        response.set_cookie('email', email)
        return response
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def registerUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(request.POST)
        print(email)
        # photos = request.POST.get('photo')
        
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already registered'}, status=400)
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        response = JsonResponse({'message': 'Registered successfully'})
        response.set_cookie('email', email)
        
        return response
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def getDashboardDetails(request):
    if request.method == 'GET':
        email = request.COOKIES.get('email')

        if not email:
            return JsonResponse({'error': 'Email not found in cookie'}, status=400)
        try:
            user = CustomUser.objects.get(email=email)
            username = user.username
            joinedClasses = user.joinedClasses
            createdClasses = user.createdClasses
            
            data = {
                'username': username,
                'joinedClasses': joinedClasses,
                'createdClasses': createdClasses
            }
            
            return JsonResponse(data)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def joinClassroom(request):
    if request.method == 'POST':
        email = request.COOKIES.get('email')  # Get email from the cookie
        
        if not email:
            return JsonResponse({'error': 'Email not found in cookie'}, status=400)
        
        classCode = request.POST.get('classCode')
        
        try:
            user = CustomUser.objects.get(email=email)
            classroom = Classroom.objects.get(code=classCode)  # Assuming you have a Classroom model with a unique code field
            
            # Add the classroom to the joinedClasses list
            user.add_joined_class(classroom.code)
            user.save()
            
            return JsonResponse({'message': 'Classroom joined successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Classroom.DoesNotExist:
            return JsonResponse({'error': 'Classroom not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def createClassroom(request):
    if request.method == 'POST':
        email = request.COOKIES.get('email')  # Get email from the cookie
        
        if not email:
            return JsonResponse({'error': 'Email not found in cookie'}, status=400)
        
        className = request.POST.get('className')
        classCode = random.randint(1000, 9999)
        try:
            user = CustomUser.objects.get(email=email)
            new_classroom = Classroom.objects.create(hostEmailId = email,name=className, code=classCode)
            
            user.add_joined_class(new_classroom.code)
            user.save()

            
            return JsonResponse({'message': 'Classroom created successfully', 'code':new_classroom.code}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def handleClassroomRequests(request, classCode):
    if request.method == 'POST':
        email = request.COOKIES.get('email')  # Get email from the cookie
    
        if not email:
            return JsonResponse({'error': 'Email not found in cookie'}, status=400)
        
        studentList = request.POST.get('studentList')
        
        try:
            user = CustomUser.objects.get(email=email)
            classDetails = Classroom.objects.get(classCode=classCode)
            # Update attendance logic here
            
            return JsonResponse({'message': 'Attendance saved successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Classroom.DoesNotExist:
            return JsonResponse({'error': 'Classroom not found'}, status=404)
    elif request.method == 'GET':
        try:
            print(classCode)
            classDetails = Classroom.objects.get(code=classCode)
            # Get class details logic here
            print(classDetails)
            
            return JsonResponse(classDetails.hostEmailId, safe=False)
        except Classroom.DoesNotExist:
            return JsonResponse({'error': 'Classroom not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)





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