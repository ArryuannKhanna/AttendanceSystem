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
from .models import CustomUser
from .models import Classroom

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            data = {
                'message': 'Login successful'
            }
            response = JsonResponse(data)
            response.set_cookie('email', email)
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def registerUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
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
            user.joinedClasses.add(classroom)
            user.save()
            
            return JsonResponse({'message': 'Classroom joined successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
        except Classroom.DoesNotExist:
            return JsonResponse({'error': 'Classroom not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def createClassroom(request):
    if request.method == 'POST':
        email = request.COOKIES.get('email')  # Get email from the cookie
        
        if not email:
            return JsonResponse({'error': 'Email not found in cookie'}, status=400)
        
        className = request.POST.get('className')
        
        try:
            user = CustomUser.objects.get(email=email)
            new_classroom = Classroom.objects.create(name=className)
            
            user.createdClasses.add(new_classroom)
            user.save()
            
            return JsonResponse({'message': 'Classroom created successfully'}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'CustomUser not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


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
            classDetails = Classroom.objects.get(classCode=classCode)
            # Get class details logic here
            
            return JsonResponse(classDetails)
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