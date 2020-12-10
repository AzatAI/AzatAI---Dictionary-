from rest_framework import serializers
from .models import *


class UsersSerializer_v1(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'email')


class UsersSerializer_v2(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'email', 'date_joined')


class DeviceSer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("__all__")


class UsersSerializer_v3(serializers.ModelSerializer):
    devices = DeviceSer(many=True)
    class Meta:
        model = Users
        fields = ('__all__')


class AuthorizationTokenSerializer(serializers.Serializer):
    account = serializers.HyperlinkedRelatedField(
        queryset=Users.objects.all(),
        required=True,
        view_name='api:account-detail',
    )

    class Meta:
        fields = ['account']