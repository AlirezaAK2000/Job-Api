from rest_framework import permissions
from .models import Employer


class IsEmployer(permissions.BasePermission):
    def has_object_permission(self , request , view , obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try: 
            # print(f'permission granted1 {obj.is_employer}')
            return obj.is_employer
        except:    
            return False
        return False
        

class IsOwner(permissions.BasePermission):
    def has_object_permission(self , request , view , obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try: 
            return request.user == obj.user
        except:    
            return False
        return False

class IsEmployee(permissions.BasePermission):
    def has_object_permission(self , request , view , obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try: 
            # print(f'permission granted1 {obj.is_employer}')
            return not obj.is_employer
        except:    
            return False
        return False