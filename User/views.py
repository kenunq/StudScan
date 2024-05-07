from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from User.models import Group, Student, Teacher
from User.permissons import IsTeacher
from User.serializers import (
    EmptySerializer,
    LoginSerializer,
    StudentListSerializer,
    StudentRetrieveSerializer,
    TeacherRetrieveSerializer,
)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)

                role = None
                role_id = None

                if hasattr(user, "student"):
                    role = "student"
                    role_id = user.student.id
                elif hasattr(user, "teacher"):
                    role = "teacher"
                    role_id = user.teacher.id

                return Response(
                    {"message": "Logged in successfully", "role": role, "role_id": role_id}, status=status.HTTP_200_OK
                )

            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    serializer_class = EmptySerializer

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


@extend_schema(tags=["Student"])
class StudentListView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = StudentListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["group__name"]

    def get_serializer_class(self):
        print(self.action)
        if self.action == "list":
            return StudentListSerializer
        return StudentRetrieveSerializer

    @extend_schema(responses=StudentRetrieveSerializer)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Teacher"])
class TeacherView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TeacherRetrieveSerializer
    permission_classes = [IsTeacher]
    queryset = Teacher.objects.all()
