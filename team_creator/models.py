from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    level = models.CharField(verbose_name="Level", max_length=200)
    tg_username = models.CharField(verbose_name="Telegram username", max_length=200)
    discord_username = models.CharField(verbose_name="Discord username", max_length=200)
    is_far_east = models.BooleanField(
        verbose_name="User from Far Eastern Federal District", default=False
    )

    def __str__(self) -> str:
        return f"Student {self.name}, {self.tg_username}"


class PM(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)
    tg_username = models.CharField(verbose_name="Telegram username", max_length=200)
    discord_username = models.CharField(verbose_name="Discord username", max_length=200)

    def __str__(self) -> str:
        return f"PM {self.name}, {self.tg_username}"
