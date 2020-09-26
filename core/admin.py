from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine,)

admin.site.unregister(User)
admin.site.register(User , UserAdmin)
admin.site.register(Employer)
admin.site.register(Employee)
admin.site.register(Advertisement)
admin.site.register(JobRequest)
