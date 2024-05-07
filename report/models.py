from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Report(models.Model):
    class StatusChoices(models.TextChoices):
        IN = "В колледже"
        OUT = "Вне колледжа"

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField("Статус", max_length=15, choices=StatusChoices)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Посещаемость"
        verbose_name_plural = "Посещаемости"

    def __str__(self):
        return self.user.first_name + self.user.last_name
