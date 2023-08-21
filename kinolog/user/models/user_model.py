import uuid

from django.db import models
from django.urls import reverse


class UserCustom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=125)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    favorite = models.ManyToManyField("films.Films", related_name="favorite")

    def __str__(self):
        return f"{self.last_name}-{self.first_name}"

    def get_absolute_url(self):
        return reverse("user", kwargs={"user_id": self.id})

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
