from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from User.models import Group, Student, Teacher


User = get_user_model()


class UserMeSetializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "first_name", "last_name", "patronymic", "birth_date", "address", "email"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class StudentListSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source="group.name")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    patronymic = serializers.ReadOnlyField(source="user.patronymic")

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "patronymic", "group", "in_college"]


class StudentRetrieveSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source="group.name")
    user = UserMeSetializer()

    class Meta:
        model = Student
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class TeacherRetrieveSerializer(serializers.ModelSerializer):
    user = UserMeSetializer()
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"


class EmptySerializer(serializers.Serializer):
    pass
