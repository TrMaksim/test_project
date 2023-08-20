from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from .models import Films


class FilmsFilter(filters.FilterSet):
    category_id = filters.UUIDFilter(field_name="category_id")
    time_release = filters.DateFilter(field_name="time_release")

    class Meta:
        model = Films
        fields = ['category_id', 'time_release']
        ordering_fields = ['category_id', 'time_release']


class FilmsPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 1000
