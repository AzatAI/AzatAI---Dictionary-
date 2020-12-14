from datetime import timedelta, datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import time
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import random


# Create your models here.

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

def get_hex_id():
    id = random.randint(1, 4294967295)
    hex_id = str(hex(id))[2:]
    return hex_id


def get_deadline():
    return datetime.now() + timedelta(days=30)



def set_id():
    while (True):
        id = get_hex_id()
        ids = UsedID.objects.all()
        used_hex_id = []
        for i in ids:
            used_hex_id.append(i.used)
        if id not in used_hex_id:
            UsedID.objects.create(used=id)
            return id
            break

        if len(used_hex_id) > 4294967295:
            raise FullMemoryException
            break


class UsedID(models.Model):
    used = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.used


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have a email")

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password, email):
        user= self.create_user(
            email=email,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Users(AbstractBaseUser):
    id = models.CharField(max_length=8, primary_key=True, unique=True, null=False)
    first_name = models.CharField(max_length=50, )
    last_name = models.CharField(max_length=50, )
    email = models.EmailField(max_length=80, unique=True)
    phone_number = PhoneNumberField(unique=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    session_expire = models.DateTimeField(default=get_deadline)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(selfs, app_label):
        return True


    def save(self, *args, **kwargs):
        # try:
        #     self.session_expire = self.last_update + timedelta(days=30)
        # except Exception:
        #     pass
        if not self.id:
            self.id = set_id()
        super(Users, self).save(*args, **kwargs)


class FullMemoryException(Exception):
    pass




class Device(models.Model):
    device_id = models.CharField(max_length=8, unique=True, null=False,primary_key=True)
    device_os = models.CharField(max_length=50)
    login_date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(Users, null=True, on_delete=models.CASCADE, default="", related_name='devices')

    def __str__(self):
        return self.device_id

    def save(self, *args, **kwargs):
        if not self.device_id:
            self.device_id = set_id()
        super(Device, self).save(*args, **kwargs)

