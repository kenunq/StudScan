from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class UserAccount(AbstractUser):
    first_name = models.CharField(
        verbose_name="имя",
        max_length=120,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=120,
        blank=True,
    )
    patronymic = models.CharField(
        verbose_name="отчество",
        max_length=120,
        blank=True,
    )

    birth_date = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
        db_index=True,
    )

    address = models.CharField(
        verbose_name="адрес",
        max_length=120,
        blank=True,
    )
    email = models.EmailField(
        verbose_name="электронная почта",
        blank=True,
        max_length=120,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name}"


class Student(models.Model):
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="student",
        verbose_name="пользователь",
    )

    elder = models.BooleanField(default=False, verbose_name="Староста")

    group = models.ForeignKey("Group", verbose_name="Группа", related_name="students", on_delete=models.CASCADE)

    in_college = models.BooleanField("В колледже", default=False)

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def clean(self):
        # teacher = getattr(self.user, "teacher", None)
        teacher = Teacher.objects.filter(user=self.user).exists()

        if teacher:
            print(teacher)
            errors = {"user": "Учитель не может быть учеником"}
            raise ValidationError(errors)

        return super().clean()


class Teacher(models.Model):
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name="пользователь",
    )

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"

    def __str__(self):
        return f"{self.id} {self.user.last_name} {self.user.patronymic} {self.user.first_name}"

    def clean(self) -> None:
        student = getattr(self.user, "student", None)
        if student:
            errors = {"user": "Ученик не может быть учителем"}
            raise ValidationError(errors)
        return super().clean()


class Group(models.Model):
    teachers = models.ForeignKey(
        "Teacher",
        on_delete=models.SET_NULL,
        verbose_name="Учителя",
        related_name="groups",
        blank=True,
        null=True,
    )

    name = models.CharField(
        "название",
        max_length=15,
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name
