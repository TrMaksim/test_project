import uuid

from django.db import models
from django.urls import reverse


class Films(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    time_release = models.DateField(auto_now_add=False, auto_now=False)
    description = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null=True)
    directors = models.ManyToManyField("Directors", related_name="creator")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("film", kwargs={"film_id": self.id})

    class Meta:
        verbose_name_plural = "Фильмы"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_id": self.id})

    class Meta:
        verbose_name_plural = "Категории"
