from rest_framework import permissions

from User.models import Teacher


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь учителем
        return request.user.is_authenticated and Teacher.objects.filter(user=request.user).exists()
