from django.contrib import admin

from User.models import Group, Student, Teacher, UserAccount


# Register your models here.


admin.site.register(UserAccount)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
