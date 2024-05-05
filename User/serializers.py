from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers


User = get_user_model()


class UserMeSetializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "first_name", "last_name", "patronymic", "birth_date", "address", "email"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
