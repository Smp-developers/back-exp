import email
import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from project_api import serializers
from project_api.models import User
from project_api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login, logout
import cloudinary.uploader
import cloudinary
from django.conf import settings
from django.core.mail import send_mail


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['password'] = user.password
        
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.

@api_view(['POST'])
def logined(request):
    try:
        if request.method == 'POST':
            email = request.data['email']
            password = request.data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                serializer = UserSerializer(user, many=False)
                return Response(serializer.data)

    except:
        return Response({"message": "Check user credentials"})


@api_view(['POST'])
def signup(request):
    data = request.data
    if request.method == 'POST':
        user = User.objects.create(
            image=request.FILES.get('image'),
            first_name=data['name'],
            year_of_graduation=data['year_of_graduation'],
            experience_in_python=data['experience'],
            email=data['email'],
            mobile=data['mobile'],
            college=data['college'],
            batch='0',
            paid_amount='0',
            batch_started='',
            meeting_url='',
            role='student',
            password=make_password(data['password']),
            Total='10000',
            referals='0',
            batch_request="not",
            social_media=data['social_media']
        )
        serializer = UserSerializer(user, many=False)
        return Response("registered success")


@api_view(['GET'])
def getting_all_students(request):
    try:
        user = User.objects.filter(role__icontains="student")
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    except:
        return Response("Data issue!!")


@api_view(['GET'])
def delete_all_students(request):
    user = User.objects.filter(role__icontains="student")
    for i in user:
        cloudinary.uploader.destroy(i.image.public_id, invalidate=True)
        i.delete()
    return Response('all students batch deleted')


# single students
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getting_single_students(request, id):
    user = User.objects.get(pk=id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# update payment


@api_view(['POST'])
def update_single_payment(request, id):
    user = User.objects.get(pk=id)
    user.paid_amount = request.data['paid_amount']
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def update_student_batch(request, id):

    user = User.objects.get(pk=id)
    
    user.batch = request.data['batch']
    user.batch_request="not"
    user.save()
    
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# meeting
@api_view(['GET'])
def delete_single_student(request, id):
    user = User.objects.get(pk=id)
    cloudinary.uploader.destroy(user.image.public_id, invalidate=True)
    user.delete()
    return Response("deleted")


@api_view(['GET'])
def get_all_batch1(request):
    user = User.objects.filter(batch__icontains="1")
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_none_batches(request):
    user = User.objects.filter(batch__icontains="0")
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_batch2(request):
    user = User.objects.filter(batch__icontains="2")
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def switch_batches(request):
    user = User.objects.filter(role__icontains="student")
    for i in user:
        if(i.batch == '1'):
            i.batch = '2'
            send_mail("Your batch update", "Your batch has been updated to batch 2 please reply to this mail for any query",
                      settings.EMAIL_HOST_USER, [i.email])
        elif(i.batch == '2'):
            i.batch = '1'
            send_mail("Your batch update", "Your batch has been updated to batch 1 please reply to this mail for any query",
                      settings.EMAIL_HOST_USER, [i.email])

        else:
            i.batch = '0'
        i.save()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_single_total(request, id):
    user = User.objects.get(pk=id)
    user.Total = request.data['total']
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def update_single_referals(request, id):
    user = User.objects.get(pk=id)
    user.referals = request.data['referals']
    cost = request.data['referals']
    if(int(cost) != 0):
        user.Total = int(user.Total)-int(cost)*500
    else:
        user.Total = '10000'
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def individual_mail(request):
    subject = request.data['subject']
    message = request.data['message']
    email_from = settings.EMAIL_HOST_USER
    recipient_list = request.data['email']
    send_mail(subject, message, email_from, [recipient_list])
    return Response("email Sent")


@api_view(['POST'])
def group_batch2_mail(request):
    subject = "Your meeting update"
    message = request.data['message']
    email_from = settings.EMAIL_HOST_USER
    meeting=request.data['meeting']
    user = User.objects.filter(batch__icontains="2")
    for i in user:
        i.meeting_url = meeting
        i.save()
        send_mail(subject, message, email_from, [i.email])
    return Response("email Sent")

@api_view(['POST'])
def sending_newStudents_mail(request):
    subject = "Your meeting update"
    message = request.data['message']
    email_from = settings.EMAIL_HOST_USER
    meeting=request.data['meeting']
    user = User.objects.filter(batch__icontains="0")
    for i in user:
        i.meeting_url = meeting
        i.save()
        send_mail(subject, message, email_from, [i.email])
    return Response("email Sent")


@api_view(['POST'])
def group_batch1_mail(request):
    subject = "Your meeting update"
    message = request.data['message']
    meeting=request.data['meeting']
    email_from = settings.EMAIL_HOST_USER
    user = User.objects.filter(batch__icontains="1")
    for i in user:
        i.meeting_url = meeting
        i.save()
        send_mail(subject, message, email_from, [i.email])
    return Response("email Sent")


@api_view(['GET'])
def delete_admin_mail(request, email):

    user = User.objects.get(email=email)
    user.delete()

    return Response("deleted user")


@api_view(['POST'])
def edit_student_profile(request, email):
    
    data=request.data
    email=request.data['email']
    user = User.objects.get(email=email)
    
    if(request.FILES.get('image')!=None):
        cloudinary.uploader.destroy(user.image.public_id, invalidate=True)
        user.image = request.FILES.get('image')
        user.save()
    user.first_name = data['name']
    user.year_of_graduation = data['year_of_graduation']
    user.experience_in_python = data['experience_in_python']
    user.mobile = data['mobile']
    user.college = data['college']
    user.social_media = data['social_media']
    user.save()
    send_mail("Your profile Update", "Your profile has been updated please check the website", settings.EMAIL_HOST_USER, [email])
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
    

@api_view(['POST'])
def check_original_password(request):
    ps=request.data['password']
    enps=request.data['enc_password']
    if(check_password(ps, enps)==True):
        return Response("success")
    else:
        return Response("fail")
    

    

def logouted(request):
    logout(request)
    return HttpResponse("you logged out bro!!")




@api_view(['POST'])
def get_batch_trainer(request):
    batch=request.data['batch']
    user=User.objects.filter(role__icontains="trainer").filter(batch__icontains=batch)
    serializer=UserSerializer(user,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def batch_request_update(request,id):
    user=User.objects.get(pk=id)
    user.batch_request="sent"
    user.save()
    serializer=UserSerializer(user,many=False)
    return Response(serializer.data)