from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from datetime import timedelta , timezone ,datetime



GENDER_CHOICE = (
    ('M' , 'male'),
    ('F' , 'female')
)

FIELDS_CHOICES = (
    ('dev' , 'development'),
    ('des' , 'design'),
    ('fam' , 'farming'),
    ('ter' , 'translating'),
    ('tra' , 'transformation'),
    ('con' , 'content management'),
    ('led' , 'leading'),
    ('acc' , 'accounting'),
    ('ins' , 'insurance')
)

STATUS_CHOICES = (
    ('s' , 'Seen'),
    ('ns' , 'Not Seen'),
    ('ac' , 'Accepted'),
    ('re' , 'Rejected')
)


def one_month_from_today():
    return datetime.now() + timedelta(days=30)

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class PhoneValidator(RegexValidator):
    regex = r'^\+?1?\d{4,30}$'
    message="Phone number must be entered in the format: '+9999'. Up to 30 digits allowed."

class Employee(models.Model):
    profile = models.OneToOneField(Profile , on_delete=models.CASCADE,null=True)
    age = models.SmallIntegerField()
    gender = models.CharField(choices=GENDER_CHOICE , max_length=1)
    resume = models.FileField(blank=True, upload_to='license')
    image = models.ImageField(default='default.jpg',upload_to = 'profile_pics')
    fields = MultiSelectField(choices=FIELDS_CHOICES , max_length=30)
    description = models.TextField(blank=True)
    phone_number = models.CharField(validators=[PhoneValidator()], max_length=32, blank=False)
    
    def __str__(self):
        return self.profile.user.username
    



class Employer(models.Model):
    profile = models.OneToOneField(Profile , on_delete=models.CASCADE , null=True)
    stablish_date = models.DateField(blank=False ,null=False)
    location = models.URLField(max_length=200 ,blank=True)
    linked_in = models.URLField(verbose_name='Linked In ',max_length=200 , blank=True)
    address = models.CharField(max_length=300 , blank=False)
    country = CountryField(blank=False)
    pic = models.ImageField(default='default.jpg',upload_to = 'profile_pics')
    phone_number = models.CharField(validators=[PhoneValidator()], max_length=32, blank=False)
    field = models.CharField(choices=FIELDS_CHOICES , max_length=3)
    def __str__(self):
        return self.profile.user.username
    


class Advertisement(models.Model):
    employer = models.ForeignKey(Employer , on_delete=models.CASCADE)
    title = models.CharField(max_length=60 , blank=False ,default='')
    ex_date = models.DateField(verbose_name="Expiration Date", default=one_month_from_today, blank=True, null=True)
    field = models.CharField(choices=FIELDS_CHOICES , max_length=3)
    salary = models.FloatField(blank=False , null=False)
    hw = models.SmallIntegerField(verbose_name='hours of work' , blank=False)
    requierments = models.TextField(blank=False)
    def __str__(self):
        return self.title
    

class JobRequest(models.Model):
    employee = models.ForeignKey(Employee , on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement , on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES , default='ns' , max_length=3)

    def __str__(self):
        return f'{self.advertisment.title} {self.pk}'