from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView, Response

from report.models import Report
from User.models import Student, Teacher, UserAccount


@extend_schema(tags=["Report"])
class UserReport(APIView):
    def post(self, request):
        data = request.data
        if data.get("user"):
            user = get_object_or_404(UserAccount, id=data["user"])
            role = "student" if Student.objects.filter(user=user).exists() else "teacher"

        if role == "student":
            student = Student.objects.get(user=user)
            status = student.in_college
            if status:
                student.in_college = False
                Report.objects.create(user=user, status="Вне колледжа")
            else:
                student.in_college = True
                Report.objects.create(user=user, status="В колледже")

            student.save()

        return Response({"status": "OK"})
