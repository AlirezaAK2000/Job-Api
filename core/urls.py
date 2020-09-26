from django.urls import path , include ,re_path

from .views import (
    AdvertismentViewSet,
    EmployeeViewSet,
    EmployerViewSet,
    JobRequestViewSet,
    RecommendedViewSet,
    home
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'ads' , AdvertismentViewSet )
router.register(r'employees' , EmployeeViewSet)
router.register(r'employers' , EmployerViewSet)
router.register(r'jobreq' , JobRequestViewSet)
router.register(r'recommended' , RecommendedViewSet)
urlpatterns = [
    path('api/token/' ,obtain_auth_token , name='token-auth' ),
    path('home/' , home , name='home')
]
urlpatterns += router.urls 

