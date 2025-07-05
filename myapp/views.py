from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from icecream import ic
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import *
from django.shortcuts import *
from datetime import datetime
from django.utils import timezone
# Create your views here.


           
# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])  
# def to_do_list(request):
#     if request.method == 'GET':
#         user = request.user
#         ic(user)
#         role = user.role
#         data = User.objects.get(user_name=user)
#         ic(data)
#         ic(role)
        
#         if role == 'USER':
#             task = Task.objects.filter(user=user)
#             ic(task)
#             serializer = TaskSerializer(task,many=True) 
#             ic(serializer.data)
#             return Response(serializer.data,status =status.HTTP_200_OK)   
#         elif role == 'ADMIN':  
#             task = Task.objects.all()
#             serializer = TaskSerializer(task,many=True)
#             return Response(serializer.data,status =status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def sign_up(request):
    data =request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    user_name = data.get('user_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not user_name:
        return Response({'message':'user_name is required'},status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({'message':'password is required'},status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(user_name=user_name).exists():
        return Response({'messsage':'user_name is already exists'})
    
    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        user_name=user_name,
        email=email,
        role=role 
    )
    user.set_password(password)
    user.save()    
    return Response({'message':'Signup Successfully'},status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def log_in(request):
    data = request.data
    user_name = data.get('user_name')
    password = data.get('password')
    # ic(password)
    if not user_name:
        return Response({'message':'user_name is required'},status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({'message':'password is required'},status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request,user_name=user_name,password=password)
    if user == None:
        return Response({"message" : "User with this credentials not exists!"}, status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    data = {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
        'user_name': user.user_name
    }
    # now = datetime.now()
    # task = get_object_or_404(Task,user__user_name=user_name)
    # if task.end_date == now:
    #     task.status == "Due"
    #     task.save()
    # ic(task)
    
    if user is not None:
        return Response({'data':data,'message':'Login Successfully'},status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'message':'invalid'},status=status.HTTP_400_BAD_REQUEST)    
        
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def to_do_list(request):
    if request.method == "POST":
        data = request.data
        user = request.user
        ic(user)
        title = data.get('title')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        task = Task.objects.create(
            user = user,
            title = title,
            description = description,
            start_date=start_date,
            end_date = end_date,
        )
        return Response({"message":"Task is successfully created"},status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        user = request.user
        now = timezone.now()
        ic(user)
        ic(Task.objects.filter(user=user))
        # task = Task.objects.filter(user=user)
        for task in Task.objects.filter(user=user):
            if not task.status == "Completed":
                ic(task.end_date)
                ic(now)
                if task.end_date <= now :
                    task.status = "Due"
                else:
                    task.status = "Pending"
                task.save()
        view_task = Task.objects.filter(user=user).values()                  
        return Response({"data":view_task},status=status.HTTP_200_OK)
    
@api_view(['POST'])
def update_to_do(request):
    user = request.user
    id = request.data.get('id')
    title = request.data.get('title')
    description =request.data.get('description')
    completed = request.data.get('completed')
    start_date =request.data.get('start_date')
    end_date = request.data.get('end_date')
    task = get_object_or_404(Task, id=id)    
    task.title = title
    task.description = description
    task.completed = completed
    task.start_date = start_date
    task.end_date = end_date
    task.save()
    return Response({"message":"Task is successfully updated"},status=status.HTTP_201_CREATED)

@api_view(['POST'])
def delete_to_do(request):
    id = request.data.get('id')
    task = get_object_or_404(Task, id=id) 
    task.delete()
    return Response({"message":"Task is deleted"},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def due_task(request):
    now = datetime.now()
    id = request.data.get('id')
    task = get_object_or_404(Task,id=id)
    if task.end_date == now:
         task.status == "Due" 
    return Response({"message":"Task is due"},status=status.HTTP_200_OK)

@api_view(['POST'])
def streak(request):
    pass

@api_view(['GET'])      
def create_superuser(request):
    User = get_user_model()
    if not User.objects.filter(user_name='admin').exists():
        User.objects.create_superuser(
            user_name='admin',
            email='monarkprajapati@gmail.com',
            password='Monark@98793',
            role = 'ADMIN'
        )
        return HttpResponse("Superuser created successfully.")
    return HttpResponse("Superuser already exists.")

from django.core.management import call_command

@api_view(['GET'])
def run_migrations_api(request):
    try:
        call_command('migrate')
        return Response({"message": "Migrations applied successfully."})
    except Exception as e:
        return Response({"error": str(e)})
        
