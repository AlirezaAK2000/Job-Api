from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django_countries.serializer_fields import CountryField
class UserSerializer(serializers.ModelSerializer):
    # pk = serializers.ReadOnlyField(source = 'pk')
    
    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'password'
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source = 'profile.user.pk')
    # pk = serializers.ReadOnlyField(source = 'pk')

    class Meta:
        model = Employee
        
        fields = [
            'profile',
            'pk',
            'age',
            'gender',
            'resume',
            'image',
            'fields',
            'description',   
        ]


class EmployerSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source = 'profile.user.pk')
    # pk = serializers.ReadOnlyField(source = 'pk')
    country = CountryField()
    class Meta:
        model = Employer
        fields = [
            'pk',
            'profile',
            'stablish_date',
            'location',
            'linked_in',
            'address',
            'country',
            'pic',
            'phone_number',
            'field',
        ]


class AdvertisementSerializer(serializers.ModelSerializer):
    employer = serializers.ReadOnlyField(source = 'employer.profile.user.pk')
    ex_date = serializers.ReadOnlyField()
    
    class Meta:
        
        model = Advertisement
        fields = [
            'pk',
            'title',
            'employer',
            'ex_date',
            'field',
            'salary',
            'hw',
            'requierments',
        ]

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source= 'user.pk')
    class Meta:
        model = Profile
        fields = [
            'pk',
            'user',
            'is_employer'
        ]

class JobRequestSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source = 'employee.profile.user.pk')
    advertisement = serializers.ReadOnlyField(source = 'advertisment.pk')

    class Meta:
        model = JobRequest
        fields = [
            'advertisement',
            'pk',
            'employee',
            'status'
        ]