from django.urls import path

from .views import FilmsAPIView, FilmsListView

urlpatterns = [
    path("films/", FilmsListView.as_view(), name="films-list"),
    path("films/<uuid:id>/", FilmsAPIView.as_view(), name="films-detail"),
]
