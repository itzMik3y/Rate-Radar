
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from django.contrib.auth import get_user_model
from base.models import *
from django.core.exceptions import ValidationError
from .serializers import *
import os
import re
from django.shortcuts import get_object_or_404
from django.db.models import Q

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        #encrypts user data in token from database
        token['email'] = user.email
        token['first_name']=user.first_name
        token['last_name']=user.last_name
       
        
        # ...

        return token

#extends serializer class
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(['POST','GET'])
def pulse(request):
    return Response('Running...')