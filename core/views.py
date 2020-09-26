from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import (
    IsEmployer,
    IsOwner,
    IsEmployee
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import action
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from collections import defaultdict


@api_view(['GET'])
def home(request):
    content = {
        'urls':[
            "admin/"
            ,r"api/token/ [name='token-auth']"
            ,r"^ads/add_advertisment/$ [name='advertisement-add-advertisment']"
            ,r"^ads/add_advertisment\.(?P<format>[a-z0-9]+)/?$ [name='advertisement-add-advertisment']"
            ,r"^ads/list_advertisment/$ [name='advertisement-list']"
            ,r"^ads/list_advertisment\.(?P<format>[a-z0-9]+)/?$ [name='advertisement-list']"
            ,r"^ads/(?P<pk>[^/.]+)/edit_advertisment/$ [name='advertisement-edit-advertisment']"
            ,r"^ads/(?P<pk>[^/.]+)/edit_advertisment\.(?P<format>[a-z0-9]+)/?$ [name='advertisement-edit-advertisment']"
            ,r"^ads/(?P<pk>[^/.]+)/remove_advertisment/$ [name='advertisement-remove-advertisment']"
            ,r"^ads/(?P<pk>[^/.]+)/remove_advertisment\.(?P<format>[a-z0-9]+)/?$ [name='advertisement-remove-advertisment']"
            ,r"^employees/add_employee/$ [name='employee-add-employee']"
            ,r"^employees/add_employee\.(?P<format>[a-z0-9]+)/?$ [name='employee-add-employee']"
            ,r"^employees/edit_emplyee/$ [name='employee-edit-emplyee']"
            ,r"^employees/edit_emplyee\.(?P<format>[a-z0-9]+)/?$ [name='employee-edit-emplyee']"
            ,r"^employees/(?P<pk>[^/.]+)/employee_panel/$ [name='employee-employee-panel']"
            ,r"^employees/(?P<pk>[^/.]+)/employee_panel\.(?P<format>[a-z0-9]+)/?$ [name='employee-employee-panel']"
            ,r"^employers/add_employer/$ [name='employer-add-employer']"
            ,r"^employers/add_employer\.(?P<format>[a-z0-9]+)/?$ [name='employer-add-employer']"
            ,r"^employers/edit_employer/$ [name='employer-edit-employer']"
            ,r"^employers/edit_employer\.(?P<format>[a-z0-9]+)/?$ [name='employer-edit-employer']"
            ,r"^employers/employers/$ [name='employer-employers']"
            ,r"^employers/employers\.(?P<format>[a-z0-9]+)/?$ [name='employer-employers']"
            ,r"^employers/(?P<pk>[^/.]+)/employer_panel/$ [name='employer-employer-panel']"
            ,r"^employers/(?P<pk>[^/.]+)/employer_panel\.(?P<format>[a-z0-9]+)/?$ [name='employer-employer-panel']"
            ,r"^jobreq/employee_requests/$ [name='jobrequest-employee-requests']"
            ,r"^jobreq/employee_requests\.(?P<format>[a-z0-9]+)/?$ [name='jobrequest-employee-requests']"
            ,r"^jobreq/(?P<pk>[^/.]+)/adv_requsts/$ [name='jobrequest-adv-requsts']"
            ,r"^jobreq/(?P<pk>[^/.]+)/adv_requsts\.(?P<format>[a-z0-9]+)/?$ [name='jobrequest-adv-requsts']"
            ,r"^jobreq/(?P<pk>[^/.]+)/apply/$ [name='jobrequest-apply']"
            ,r"^jobreq/(?P<pk>[^/.]+)/apply\.(?P<format>[a-z0-9]+)/?$ [name='jobrequest-apply']"
            ,r"^jobreq/(?P<pk>[^/.]+)/req_status/$ [name='jobrequest-req-status']"
            ,r"^jobreq/(?P<pk>[^/.]+)/req_status\.(?P<format>[a-z0-9]+)/?$ [name='jobrequest-req-status']"
            ,r"^recommended/recommended_offers/$ [name='advertisement-recommended-offers']"
            ,r"^recommended/recommended_offers\.(?P<format>[a-z0-9]+)/?$ [name='advertisement-recommended-offers']"
            ,r"^$ [name='api-root']"
            ,r"^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']"
            ,r"api-auth/"
            ,r"^rest-auth/"
            ,r"^rest-auth/registration/"
            ,r"^media/(?P<path>.*)$"
            ,r"^static/(?P<path>.*)$"
        ]
    }
    return Response(data=content)



class AdvertismentViewSet(viewsets.GenericViewSet):
    queryset = Advertisement.objects.all()
    permission_classes = [IsEmployer, IsAuthenticated, IsOwner]

    def binary_search(self, qs, salary, left, right):
        if right < left:
            return None

        mid = (left + right)//2
        print(f'{mid}')
        if qs[mid].salary == salary:
            return mid
        elif qs[mid].salary > salary:
            return self.binary_search(qs, salary, left, mid-1)
        else:
            return self.binary_search(qs, salary, mid+1, right)

    def get_object_by_pk(self, pk):
        try:
            return Advertisement.objects.get(pk=pk)
        except Advertisement.DoesNotExist:
            raise Http404

    def check_pers(self, request, adv=None):
        profile = None
        if not adv:
            profile = get_object_or_404(Profile, user=request.user)
        else:
            profile = get_object_or_404(
                Profile, user=adv.employer.profile.user)
        self.check_object_permissions(request, profile)
        return profile

    @action(methods=['GET'], detail=False, url_path='', url_name='list')
    def list_advertisment(self, request, *args, **kwargs):
        # print(f'***** {request.GET}')
        params = defaultdict(lambda: None, request.GET)
        ads = None
        if params['title']:
            title = params['title']
            ads = Advertisement.objects.filter(title__in=title)
        elif params['field']:
            field = params['field']
            if ads:
                ads += Advertisement.objects.filter(field__in=field)
            else:
                ads = Advertisement.objects.filter(field__in=field)
        elif params['min_salary'] and params['max_salary']:
            qs = Advertisement.objects.order_by('salary')

            min_valid, max_valid = qs[0].salary, qs[len(qs)-1].salary
            min_salary, max_salary = float(
                params['min_salary'][0]), float(params['max_salary'][0])
            min_index = self.binary_search(
                qs, min_salary, 0, len(qs)) if min_salary > min_valid else 0
            max_index = self.binary_search(
                qs, max_salary, 0, len(qs)) if max_salary < max_valid else len(qs) - 1
            if not (min_index is None or max_index is None):
                ads = qs[min_index:max_index+1]

        else:
            ads = Advertisement.objects.all()

        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def add_advertisment(self, request):
        profile = self.check_pers(request)
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=Employer.objects.get(
                profile=profile), ex_date=one_month_from_today())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=True)
    def edit_advertisment(self, request, pk):
        adv = self.get_object_by_pk(pk=pk)
        self.check_pers(request)
        serializer = AdvertisementSerializer(adv, data=request.data)
        if serializers.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True)
    def remove_advertisment(self, request, pk):
        adv = self.get_object_by_pk(pk)
        self.check_pers(request, adv=adv)
        adv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeViewSet(viewsets.GenericViewSet):
    queryset = Employee.objects.all()

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def add_employee(self, request):
        has_profile = Profile.objects.filter(user=request.user).exists()
        serializer = EmployeeSerializer(data=request.data)
        if has_profile:
            profile = Profile.objects.get(user=request.user)
            has_account = Employee.objects.filter(profile=profile).exists()
            if not has_account:
                profile.is_employer = False
                profile.save()
                if serializer.is_valid():
                    serializer.save(profile=profile)
                    content = {
                        'message': 'successfully added'
                    }
                    return Response(data=content)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {
                    'operation': 'you already have an account'
                }

        else:
            profile = Profile(user=request.user, is_employer=False)
            profile.save()
            if serializer.is_valid():
                serializer.save(profile=profile)
                content = {
                    'message': 'successfully added'
                }
                return Response(data=content)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def edit_emplyee(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            employe = Employee.objects.get(profile=profile)
            serializer = EmployeeSerializer(employe, data=request.data)
            if serializers.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            content = {
                'message': "profile doesn't exist"
            }
            return Response(data=content)
        except Employee.DoesNotExist:
            content = {
                'message': "employee doesn't exist"
            }
            return Response(data=content)

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def employee_panel(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, many=False)
        return Response(data=serializer.data)


class EmployerViewSet(viewsets.GenericViewSet):
    queryset = Employer.objects.all()

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
    def add_employer(self, request):
        has_profile = Profile.objects.filter(user=request.user).exists()
        serializer = EmployerSerializer(data=request.data)
        if has_profile:
            profile = Profile.objects.get(user=request.user)
            has_account = Employer.objects.filter(profile=profile).exists()
            if not has_account:
                profile.is_employer = False
                profile.save()
                if serializer.is_valid():
                    serializer.save(profile=profile)
                    content = {
                        'message': 'successfully added'
                    }
                    return Response(data=content)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {
                    'operation': 'you already have an account'
                }
                return Response(data=content)
        else:
            profile = Profile(user=request.user, is_employer=False)
            profile.save()
            if serializer.is_valid():
                serializer.save(profile=profile)
                content = {
                    'message': 'successfully added'
                }
                return Response(data=content)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated])
    def edit_employer(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            employe = Employer.objects.get(profile=profile)
            serializer = EmployerSerializer(employe, data=request.data)
            if serializers.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            content = {
                'message': "profile doesn't exist"
            }
            return Response(data=content)
        except Employer.DoesNotExist:
            content = {
                'message': "employer doesn't exist"
            }
            return Response(data=content)

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def employer_panel(self, request, pk):
        employer = get_object_or_404(Employee, pk=pk)
        serializer = EmployerSerializer(employer, many=False)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def employers(self, request):
        employer = Employer.objects.all()
        serializer = EmployerSerializer(employer, many=True)
        return Response(data=serializer.data)


class JobRequestViewSet(viewsets.GenericViewSet):
    queryset = JobRequest.objects.all()

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated, IsEmployee])
    def employee_requests(self, request):
        profile = Profile.objects.get(user=request.user)
        self.check_object_permissions(request, profile)
        employee = Employee.objects.get(profile=profile)
        reqs = JobRequest.objects.filter(employee=employee)
        serializer = JobRequestSerializer(reqs, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated, IsOwner])
    def adv_requsts(self, request, pk):
        adv = get_object_or_404(Advertisement, pk=pk)
        self.check_object_permissions(request, adv.employer.profile)
        reqs = JobRequest.objects.filter(advertisement=adv)
        serialier = JobRequestSerializer(reqs, many=True)
        return Response(serialier.data)

    @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated, IsOwner])
    def req_status(self, request, pk):
        req = get_object_or_404(JobRequest, pk=pk)
        self.check_object_permissions(
            request, req.advertisement.employer.profile)
        serializer = JobRequestSerializer(req, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'message': 'status changed successfuly'
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated, IsEmployee])
    def apply(self, request, pk):
        profile = Profile.objects.get(user=request.user)
        self.check_object_permissions(request, profile)
        adv = Advertisement.objects.get(pk=pk)
        employee = Employee.objects.get(profile=profile)
        serializer = JobRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee, advertisement=adv)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendedViewSet(viewsets.GenericViewSet):
    queryset = Advertisement.objects.all()
    permission_classes = [IsEmployee, IsAuthenticated]

    @action(methods=['GET'], detail=False)
    def recommended_offers(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        try:
            employee = Employee.objects.get(profile=profile)
            print(employee.fields)
            ads = Advertisement.objects.filter(field__in=list(employee.fields))
            serializer = AdvertisementSerializer(ads, many=True)
            return Response(data = serializer.data)
        except Employee.DoesNotExist:
            return Response(data = {
                'message': 'you are not an employee'
            })

