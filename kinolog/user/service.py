from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from .models import UserCustom


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name="first_name")
    phone = filters.CharFilter(field_name="phone")

    class Meta:
        model = UserCustom
        fields = (
            "first_name",
            "phone",
        )
        ordering_fields = (
            "first_name",
            "phone",
        )


class UserPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 1000
