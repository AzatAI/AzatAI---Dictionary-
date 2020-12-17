import platform
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
import sys
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from .serializers import *
import re
from .utils import *
from django.core.exceptions import *
'''Functions'''



def get_time_pass():
    time_pass = str(datetime.now())[14:16]
    time_pass += str(int(time_pass) + 1) + time_pass
    if len(time_pass) < 6:
        time_pass1 = ""
        for i in range(len(time_pass)):
            time_pass1 += time_pass[i]
            if i == 1:
                time_pass1 += "0"
        time_pass = time_pass1
    return time_pass


def get_header(request):
    regex = re.compile('^HTTP_')
    head = dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))
    return head


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

'''Views'''



class Main(View):
    def get(self, request):

        return redirect('dict_main_url')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('dict_main_url')


class Registration(View):
    def post(self, request):
        form = RegistrationForm()
        bound_form = RegistrationForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            obj_cleaned = bound_form.cleaned_data.get('email')
            raw_password = bound_form.cleaned_data.get('password1')
            account = authenticate(email_or_phone=obj_cleaned, password=raw_password)
            login(request, account)
            ip = get_client_ip(request)
            os = str(request.user_agent.os.family) + " " + str(request.user_agent.os.version_string)
            user = Users.objects.get(id__iexact=request.user.id)
            Device.objects.create(ip=ip, device_os=os, user=user)

            return redirect('dict_main_url')
        # return render(request, "azatAI/registration.html", context={'form': bound_form,  })
        return redirect('dict_main_url')


    def get(self, request):

        user = request.user
        if user.is_authenticated:
            return redirect('main_url')
        form = RegistrationForm()

        return render(request, "azatAI/registration.html", context={'form': form })


class Login(View):
    def post(self, request):
        bound_form = LogForm(request.POST)
        email_or_phone = request.POST['email_or_phone']
        password = request.POST['password']
        if bound_form.is_valid():
            user = authenticate(email_or_phone=email_or_phone, password=password)
            if user:
                login(request, user)
                user = Users.objects.get(id=request.user.id)
                user.last_update = datetime.now()
                user.last_login = datetime.now()
                user.save()

            return redirect('dict_main_url')
        return redirect('dict_main_url')

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('main_url')
        form_log = LogForm()

        return render(request, 'azatAI/Login.html', context={'form_log': form_log})


'''Api Interfaces'''


class UsersView(APIView):
    def get(self, request, ver):
        users = Users.objects.filter(is_active=True)
        user_ver = 'UsersSerializer_' + ver
        user_ver = str_to_class(user_ver)
        serializer = user_ver(users, many=True)

        return Response(serializer.data)


class DeviceView(APIView):
    def get(self, request,):
        devices = Device.objects.all()
        serializer = DeviceSer(devices, many=True)

        return Response(serializer.data)

