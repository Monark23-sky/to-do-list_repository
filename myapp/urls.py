from django.urls import path
from .views import *
from django.http import HttpResponse
from django.contrib.auth import get_user_model



urlpatterns = [
    path('to_do_list/',to_do_list,name='to_do_list'),
    path('sign_up/',sign_up,name='sign_up'),
    path('log_in/',log_in,name='log_in'),
    path('update_to_do/',update_to_do,name='update_to_do'),
    path('delete_to_do/',delete_to_do,name='delete_to_do'),
    path('due_task/',due_task,name='due_task'),
    path('create-admin/', create_superuser,name='create_superuser'),  # 🚨 Remove this after it's used!

]