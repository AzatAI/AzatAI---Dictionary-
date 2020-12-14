from rest_framework import serializers
from .models import *

# class WordSerializer_v1(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ('id', 'email')
#
#
# class WordSerializer_v2(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ('id', 'email', 'date_joined')


class WordSerializer_v1(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('__all__')


class AuthorizationTokenSerializer(serializers.Serializer):
    words = serializers.HyperlinkedRelatedField(
        queryset=Word.objects.all(),
        required=True,
        view_name='api:account-detail',
    )

    class Meta:
        fields = ['words']