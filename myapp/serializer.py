# from rest_framework import serializers
# from .models import *

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["user_name"]

# class TaskSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only = True)
#     user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
#     class Meta:
#         model = Task
#         fields = '__all__'

