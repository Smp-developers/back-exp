from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from project_api import serializers
from project_api.models import Courses, Trainees, User
from project_api.serializers import CourseSerializer, TraineeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
import cloudinary.uploader
import cloudinary


@api_view(['POST'])
def course_upload(request):

    course = Courses.objects.create(
        image=request.FILES.get('image'),
        course_name=request.data['course_name'],
        course_author=request.data['course_author'],
       
    )
    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def delete_all_courses(request):
    course = Courses.objects.all()
    for i in course:
        cloudinary.uploader.destroy(i.image.public_id, invalidate=True)
        cloudinary.uploader.destroy(i.author_image.public_id, invalidate=True)
        i.delete()

    return Response("all deleted")


@api_view(['GET'])
def delete_single_course(request, id):
    course = Courses.objects.get(pk=id)
    cloudinary.uploader.destroy(course.image.public_id, invalidate=True)
    
    course.delete()

    return Response("deleted")


@api_view(['GET'])
def get_single_course(request, id):
    course = Courses.objects.get(pk=id)

    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def edit_single_course(request, id):
    course = Courses.objects.get(pk=id)
    if(request.FILES.get('image') != None):
        cloudinary.uploader.destroy(course.image.public_id, invalidate=True)
        course.image = request.FILES.get('image')
        course.save()
    course.course_name = request.data['course_name']
    course.course_author = request.data['course_author']
    
    course.save()

    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_courses(request):
    course = Courses.objects.all()
    serializer = CourseSerializer(course, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def author_name_course(request, id):
    course = Courses.objects.filter(pk=id)
    course.author_name = request.data['author_name']
    course.author_designation = request.data['author_designation']
    course.save()
    serializer = CourseSerializer(course, many=False)
    return Response(serializer.data)





# Trainee views



@api_view(['POST'])
def upload_trainee(request):
    trainee = User.objects.create(
        image=request.FILES.get('image'),
        first_name=request.data['name'],
        skills=request.data['skills'],
        company=request.data['company'],
        mobile=request.data['mobile'],
        batch=request.data['batch'],
        email=request.data['email'],
        paid_amount='NA',
        Total='NA',
        referals='NA',
        role='trainer',
        password=make_password('Trainer@1')
       
    )

    serializer = UserSerializer(trainee, many=False)
    return Response(serializer.data)






@api_view(['POST'])
def edit_single_trainee(request, id):
    trainee = User.objects.get(pk=id)
    if(request.FILES.get('image') != None):
        cloudinary.uploader.destroy(trainee.image.public_id, invalidate=True)
        trainee.image = request.FILES.get('image')
        trainee.save()

    trainee.name = request.data['name']
    trainee.designation = request.data['designation']
    trainee.company = request.data['company']
    trainee.mobile = request.data['mobile']
    trainee.batch = request.data['batch']

    trainee.experience_field = request.data['experience_field']

    trainee.save()

    serializer = TraineeSerializer(trainee, many=False)
    return Response(serializer.data)



@api_view(['GET'])
def get_all_trainees(request):
    trainee = User.objects.filter(role__icontains="trainer")
    serializer=UserSerializer(trainee, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_single_trainee(request,id):
    trainee = User.objects.get(pk=id)
    serializer = UserSerializer(trainee, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def delete_single_trainee(request,id):
    trainee = User.objects.get(pk=id)
    trainee.delete()
    return Response("deleted trainee")




@api_view(['POST'])
def changePassword(request,email):
    user = User.objects.get(email=email)
    password=request.data['password']
    user.password=make_password(password)
    user.save()
    serializer=UserSerializer(user,many=False)
    return Response("changed password ")





