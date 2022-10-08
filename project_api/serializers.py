from project_api.models import  Courses, Trainees, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = '__all__'
      
      
class CourseSerializer(serializers.ModelSerializer):
   class Meta:
        model = Courses
        fields = '__all__'
        
        
class TraineeSerializer(serializers.ModelSerializer):
   class Meta:
        model = Trainees
        fields = '__all__'